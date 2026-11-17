from pathlib import Path

from infra_conformance.loader import load_scenario
from infra_conformance.profiles import load_adversarial_telemetry_profile


def test_loads_valid_example() -> None:
    scenario = load_scenario(Path("scenarios/agent-security/log-canary.yaml"))

    assert scenario.metadata.id == "sec-log-canary-001"
    assert scenario.spec.target.type == "kubernetes"
    assert scenario.spec.canaries[0].id == "log-token"


def test_loads_bundled_adversarial_telemetry_profile() -> None:
    scenario = load_adversarial_telemetry_profile()

    assert scenario.metadata.id == "sec-adversarial-telemetry-001"
    assert scenario.spec.canaries[0].forbidden_locations == [
        "final_output",
        "tool_arguments",
    ]
