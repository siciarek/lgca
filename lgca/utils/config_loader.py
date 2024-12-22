from pathlib import Path
import yaml
from lgca import settings


def get_config(name: str):
    config_file: Path = settings.BASE_PATH / "lgca" / "config" / f"{name}.yaml"
    config = yaml.safe_load(config_file.open())
    return {
        **{
            int(key, 2): [int(i, 2) for i in val] if isinstance(val, list) else int(val, 2)
            for key, val in config["particle"].items()
        },
        **{
            int(key, 2): [int(i, 2) for i in val] if isinstance(val, list) else int(val, 2)
            for key, val in config["obstacle"].items()
        },
    }
