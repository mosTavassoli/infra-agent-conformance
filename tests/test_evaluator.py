from pathlib import Path

from infra_conformance.evaluator import evaluate_canary_leakage
from infra_conformance.loader import load_scenario


def _scenario():  # type: ignore[no-untyped-def]
    return load_scenario(Path("scenarios/agent-security/log-canary.yaml"))


def test_passes_when_canary_is_absent() -> None:
    result = evaluate_canary_leakage(
        _scenario(),
        {"model_response": "The configuration is missing."},
    )

    assert result.status == "pass"
    assert result.findings[0].status == "pass"


def test_fails_when_canary_leaks() -> None:
    result = evaluate_canary_leakage(
        _scenario(),
        {"model_response": "Leaked SYNTHETIC_CANARY_7F3A91D2"},
    )

    assert result.status == "fail"
    assert result.findings[0].evidence_locations == ["model_response"]
