from pathlib import Path
import yaml
from lgca import settings


def get_config(name: str):
    particle_config_file: Path = settings.LGCA_CONFIGURATION_PATH / f"{name}.yaml"
    particle_config: dict = yaml.safe_load(particle_config_file.open())

    obstacle_config_file: Path = settings.LGCA_CONFIGURATION_PATH / "obstacles" / "wall.yaml"
    temp: dict = yaml.safe_load(obstacle_config_file.open())
    obstacle_config = temp.get(name) if name in temp else temp.get(name.split("_")[0])

    return {
        **{
            int(key, 2): [int(i, 2) for i in val] if isinstance(val, list) else int(val, 2)
            for key, val in particle_config.items()
        },
        **{
            int(key, 2): [int(i, 2) for i in val] if isinstance(val, list) else int(val, 2)
            for key, val in obstacle_config.items()
        },
    }
