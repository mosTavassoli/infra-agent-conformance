from pathlib import Path

from infra_conformance.loader import load_scenario


def test_loads_valid_example() -> None:
    scenario = load_scenario(Path("scenarios/agent-security/log-canary.yaml"))

    assert scenario.metadata.id == "sec-log-canary-001"
    assert scenario.spec.target.type == "kubernetes"
    assert scenario.spec.canaries[0].id == "log-token"
