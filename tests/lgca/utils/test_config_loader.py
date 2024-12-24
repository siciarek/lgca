from pathlib import Path
import yaml
import pytest
from lgca import settings
from lgca.utils.config_loader import get_config

models = (
    ("hpp", 16, 16, 2),
    ("fhp_i", 64, 64, 5),
    ("fhp_ii", 128, 64, 22),
    ("fhp_iii", 128, 64, 76),
)


@pytest.mark.parametrize("name,state_count,obstacle_rule_count,collision_count", models)
def test_collisions(name, state_count, obstacle_rule_count, collision_count):
    config_file: Path = settings.BASE_PATH / "lgca" / "config" / "collisions.yaml"
    config = yaml.safe_load(config_file.open())
    assert len(config[name]) == collision_count


@pytest.mark.parametrize("name,state_count,obstacle_rule_count,collision_count", models)
def test_get_config(name, state_count, obstacle_rule_count, collision_count):
    config = get_config(name=name)
    assert isinstance(config, dict)
    particle_rules = {key: val for key, val in config.items() if key < 128}
    obstacle_rules = {key: val for key, val in config.items() if key >= 128}
    collision_rules = {key: val for key, val in particle_rules.items() if key != val}
    assert len(particle_rules) == state_count, particle_rules
    assert len(obstacle_rules) == obstacle_rule_count, obstacle_rules
    assert len(collision_rules) == collision_count, collision_rules
