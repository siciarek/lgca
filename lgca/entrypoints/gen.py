import glob
import subprocess
from pathlib import Path
import contextlib
import numpy as np
import click
import ffmpy
from PIL import Image
from lgca.automata import (
    Hpp,
)
from lgca.utils.common import decode_pattern_file, get_color_map
from lgca.utils.table_generator import BIT_COUNT


def generate_frames(
    model_name,
    input_grid: list,
    automaton,
    tile_size: int,
    color_map,
    steps: int,
    animated_source_file_tmpl: str,
    step_tmpl: str,
):
    while True:
        bitmap_array: list = []

        for row in input_grid:
            bitmap_array.append([color_map[cell] for cell in row])

        img: Image = Image.fromarray(np.array(np.uint8(bitmap_array)))
        img = img.resize(size=[elem * tile_size for elem in img.size], resample=Image.Resampling.NEAREST)
        img.save(animated_source_file_tmpl.format(model_name=model_name, step=automaton.step))

        print(step_tmpl.format(step=automaton.step), end="\r")

        if automaton.step == steps:
            break

        next(automaton)


def generate_animation(fmt: str, source_files: str, target_file: str, fps: int):
    # use exit stack to automatically close opened images
    with contextlib.ExitStack() as stack:
        source_images = sorted(glob.glob(source_files))

        # lazily load images
        imgs = (stack.enter_context(Image.open(f)) for f in source_images)

        # extract  first image from iterator
        img = next(imgs)

        duration = 50

        if fps > 0:
            duration = 10000 / fps

        # https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif
        img.save(fp=target_file, format=fmt, append_images=imgs, save_all=True, duration=duration)


@click.command()
@click.option("-s", "--steps", default=0, show_default=True, help="Number of steps.")
@click.option(
    "-n", "--model-name", type=click.Choice(["HPP", "hpp"]), show_default=True, default="hpp", help="Model name."
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
def main(steps: int, model_name: str, pattern: str, animation: bool):
    """Generate image of LGCA."""

    click.echo(f"{model_name=} {pattern=} {steps=} {animation=}")

    pattern_file = Path(pattern)
    if not pattern_file.is_file():
        raise click.FileError(pattern_file.as_posix(), "pattern not found.")

    step_tmpl = f"STEP: {{step:0{len(str(steps))}}}"
    file_tmpl = f"{pattern_file.stem}-{{model_name}}-{{step:0{len(str(steps))}}}.png"

    animated_source_file_tmpl = f".animated/{pattern_file.stem}-{{model_name}}-{{step:0{len(str(steps))}}}.png"
    animated_glob_file_tmpl = f".animated/{pattern_file.stem}-{{model_name}}-*.png"
    animated_target_file_tmpl = f".animated/{pattern_file.stem}-{{model_name}}.gif"

    input_grid, tile_size, mode, fps, obstacle_color = decode_pattern_file(
        pattern_file=pattern_file,
        model_name=model_name,
    )
    color_map = get_color_map(bit_count=BIT_COUNT[model_name], obstacle_color=obstacle_color)

    if model_name == "hpp":
        automaton = Hpp(
            grid=input_grid,
            mode=mode,
        )
    else:
        raise click.ClickException(f"Model {model_name} is not supported yet.")

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
        Path(".animated").mkdir(parents=True, exist_ok=True)

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
        )

        click.secho(f"CREATE ANIMATED FILE ({animation})...", fg="green")
        target_file = animated_target_file_tmpl.format(model_name=model_name)
        target_file_mp4 = target_file.replace(".gif", ".mp4")
        Path(target_file).unlink(missing_ok=True)
        Path(target_file_mp4).unlink(missing_ok=True)

        generate_animation(
            fmt="GIF",
            source_files=animated_glob_file_tmpl.format(model_name=model_name),
            target_file=target_file,
            fps=fps,
        )

        if animation == "mp4":
            click.secho("CONVERT gif -> mp4", fg="green")
            ret_code = subprocess.call(["which", "ffmpeg"])
            if ret_code == 0:
                ffmpy.FFmpeg(inputs={target_file: None}, outputs={target_file_mp4: None}).run()
            else:
                click.ClickException("Conversion gif -> mp4 requires ffmpeg installed in your system.")

        click.secho("MAKE TIDY...", fg="green")
        for temp_file in Path(".animated").glob("*.png"):
            temp_file.unlink()

        if animation == "mp4":
            Path(target_file).unlink()
