from functools import cache
from importlib import resources

import yaml

from infra_conformance.loader import parse_scenario
from infra_conformance.models import Scenario


@cache
def load_adversarial_telemetry_profile() -> Scenario:
    """Load the bundled security profile used by the bounded DevOps Bench experiment."""
    profile = resources.files(__package__).joinpath("adversarial-telemetry-v1.yaml")
    raw = yaml.safe_load(profile.read_text(encoding="utf-8"))
    return parse_scenario(raw)
