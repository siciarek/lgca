import glob
import tempfile
import shutil
import subprocess
from pathlib import Path
import contextlib
import numpy as np
import click
import ffmpy
from PIL import Image
from lgca import settings
from lgca.automata import (
    Hpp,
    Lbm,
)
from lgca.utils.common import decode_pattern_file, get_color_map
from lgca.utils.table_generator import BIT_COUNT

MODELS = {
    "hpp": Hpp,
    "lbm": Lbm,
}


def generate_frames(
    model_name,
    input_grid: list,
    automaton,
    tile_size: int,
    color_map,
    steps: int,
    animated_source_file_tmpl: str,
    step_tmpl: str,
    save_every: int,
):
    while True:
        bitmap_array: list = []

        if automaton.step % save_every == 0:
            for row in input_grid:
                bitmap_array.append([color_map[cell] for cell in row])

            img: Image = Image.fromarray(np.array(np.uint8(bitmap_array)))
            img = img.resize(size=[elem * tile_size for elem in img.size], resample=Image.Resampling.NEAREST)
            img.save(animated_source_file_tmpl.format(model_name=model_name, step=automaton.step))

            print(step_tmpl.format(step=automaton.step), end="\r")

            if automaton.step >= steps:
                break

        next(automaton)


def generate_animation(fmt: str, source_files: str, animation_temp_file: str, fps: int):
    # use exit stack to automatically close opened images
    with contextlib.ExitStack() as stack:
        source_images = sorted(glob.glob(source_files))

        # lazily load images
        imgs = (stack.enter_context(Image.open(f)) for f in source_images)

        # extract  first image from iterator
        img = next(imgs)

        duration = 60

        if fps > 0:
            duration = 1000 // fps

        # https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif
        img.save(fp=animation_temp_file, format=fmt, append_images=imgs, save_all=True, duration=duration)


@click.command()
@click.option("-s", "--steps", default=0, show_default=True, help="Number of steps.")
@click.option(
    "-e", "--save-every", default=1, show_default=True, help="In animation save every specified number of steps."
)
@click.option(
    "-n",
    "--model-name",
    type=click.Choice(["HPP", "LBM", "hpp", "lbm"]),
    show_default=True,
    default="hpp",
    help="Model name.",
)
@click.option(
    "-p",
    "--pattern",
    default="",
    type=str,
    show_default=False,
    help="Select initial state pattern.",
)
@click.option("-a", "--animation", type=click.Choice(["gif", "mp4"]), show_default=True, help="Animated file format.")
def main(steps: int, save_every: int, model_name: str, pattern: str, animation: bool):
    """Generate image of LGCA."""

    """
    PERFORMANCE:
    (Mon Dec 30 13:15:38 CET 2024)
    time gen -n lbm -p lgca/data/patterns/lbm/obstacle.json --animation=mp4 --save-every=30 --steps=10000
    119.13s user
    7.34s system
    107% cpu
    1:57.92 total
    """

    click.echo(f"{model_name=} {save_every=}, {pattern=} {steps=} {animation=}")

    pattern_file = Path(pattern)
    if not pattern_file.is_file():
        raise click.FileError(pattern_file.as_posix(), "pattern not found.")

    step_tmpl = f"FRAME: {{step:0{len(str(steps))}}}/{steps}"
    file_tmpl = f"{pattern_file.stem}-{{model_name}}-{{step:0{len(str(steps))}}}.png"

    input_grid, tile_size, mode, fps, obstacle_color = decode_pattern_file(
        pattern_file=pattern_file,
        model_name=model_name,
    )
    color_map = (
        ([(i, i * 2 % 0xFF, i) for i in range(0x100)])
        if model_name == "lbm"
        else get_color_map(bit_count=BIT_COUNT[model_name], obstacle_color=obstacle_color)
    )

    if model_name not in MODELS:
        raise click.ClickException(f"Model {model_name} is not supported yet.")

    automaton = MODELS[model_name](
        grid=input_grid,
        mode=mode,
    )

    if animation is None:
        click.secho(f"CREATE AUTOMATON STAGE ({steps})...", fg="green")
        while True:
            print(step_tmpl.format(step=automaton.step), end="\r")
            if automaton.step == steps:
                break
            next(automaton)

        bitmap_array: list = []
        for row in input_grid:
            bitmap_array.append([color_map[cell] for cell in row])

        img: Image = Image.fromarray(np.array(np.uint8(bitmap_array)))
        img = img.resize(size=[elem * tile_size for elem in img.size], resample=Image.Resampling.NEAREST)
        img.save(file_tmpl.format(model_name=model_name, step=automaton.step))
    else:
        with tempfile.TemporaryDirectory() as tmpdirname:
            animated_dir = Path(tmpdirname)
            animated_dir.mkdir(parents=True, exist_ok=True)

            animated_source_file_tmpl = (
                animated_dir / f"{pattern_file.stem}-{{model_name}}-{{step:0{len(str(steps))}}}.png"
            ).as_posix()
            animated_glob_file_tmpl = (animated_dir / f"{pattern_file.stem}-{{model_name}}-*.png").as_posix()
            animated_animation_temp_file_tmpl = (
                animated_dir / f"{pattern_file.stem}-{{model_name}}-{steps}.gif"
            ).as_posix()

            click.secho(f"CREATE ANIMATION FRAMES ({steps})...", fg="green")

            generate_frames(
                model_name=model_name,
                input_grid=input_grid,
                automaton=automaton,
                tile_size=tile_size,
                color_map=color_map,
                steps=steps,
                animated_source_file_tmpl=animated_source_file_tmpl,
                step_tmpl=step_tmpl,
                save_every=save_every,
            )

            click.secho(f"CREATE ANIMATED FILE ({animation})...", fg="green")
            animation_temp_file = animated_animation_temp_file_tmpl.format(model_name=model_name)

            if animation == "gif":
                animation_target_file = animation_temp_file
            elif animation == "mp4":
                animation_target_file = animation_temp_file.replace(".gif", ".mp4")

            Path(animation_temp_file).unlink(missing_ok=True)
            Path(animation_target_file).unlink(missing_ok=True)

            generate_animation(
                fmt="GIF",
                source_files=animated_glob_file_tmpl.format(model_name=model_name),
                animation_temp_file=animation_temp_file,
                fps=fps,
            )

            if animation == "gif":
                animation_target_file = animation_temp_file
            elif animation == "mp4":
                click.secho("CONVERT gif -> mp4", fg="green")
                ret_code = subprocess.call(["which", "ffmpeg"])
                if ret_code == 0:
                    ffmpy.FFmpeg(inputs={animation_temp_file: None}, outputs={animation_target_file: None}).run()
                else:
                    click.ClickException("Conversion gif -> mp4 requires ffmpeg installed in your system.")

            click.secho("MAKE TIDY...", fg="green")

            for temp_file in animated_dir.glob("*.png"):
                temp_file.unlink()

            temp_file = settings.BASE_PATH / Path(animation_temp_file).name
            temp_file.unlink(missing_ok=True)

            temp_file = settings.BASE_PATH / Path(animation_target_file).name.replace(".gif", ".mp4")
            temp_file.unlink(missing_ok=True)

            shutil.move(animation_target_file, settings.BASE_PATH / Path(animation_target_file).name)
