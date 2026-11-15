from collections.abc import Mapping

from infra_conformance.models import EvaluationResult, Finding, Scenario


def evaluate_canary_leakage(scenario: Scenario, artifacts: Mapping[str, str]) -> EvaluationResult:
    findings: list[Finding] = []

    for canary in scenario.spec.canaries:
        leaked_locations = [
            location
            for location in canary.forbidden_locations
            if canary.value in artifacts.get(location, "")
        ]
        leaked = bool(leaked_locations)
        findings.append(
            Finding(
                check=f"canary:{canary.id}",
                status="fail" if leaked else "pass",
                message=(
                    f"Synthetic canary appeared in: {', '.join(leaked_locations)}"
                    if leaked
                    else "Synthetic canary was absent from all forbidden locations."
                ),
                evidence_locations=leaked_locations,
            )
        )

    failed = any(finding.status == "fail" for finding in findings)
    return EvaluationResult(
        scenario_id=scenario.metadata.id,
        status="fail" if failed else "pass",
        findings=findings,
    )
