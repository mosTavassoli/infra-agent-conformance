# Infrastructure Agent Conformance

An open-source conformance platform for testing whether infrastructure agents diagnose failures usefully and safely.

The first suite focuses on Kubernetes AI agents and measures deterministic security properties alongside diagnosis quality, evidence grounding, safe abstention, latency, and cost.

## Why

Read-only access limits direct damage, but it does not answer whether an agent can expose sensitive context, follow hostile instructions embedded in logs, exceed its intended scope, or produce unsupported conclusions. These claims should be tested with reproducible scenarios.

## Current foundation

The repository currently provides:

- A versioned scenario contract
- YAML scenario validation
- Deterministic synthetic-canary leakage evaluation
- Deterministic hostile-telemetry and forbidden-operation evaluation
- A bounded external metric and task fixture for Kubernetes SIGs DevOps Bench
- Versioned JSON results
- A CLI suitable for local use and CI
- Initial architecture, security, and product documentation

The core package does not create clusters or run AI agents. The bounded proof of concept delegates
those responsibilities to DevOps Bench rather than implementing another runner.

Further standalone runner development is paused while the project validates whether its security-conformance scenarios should be contributed to or integrated with established benchmarks such as Kubernetes SIGs DevOps Bench. See the [validation plan](docs/product/validation-plan.md) and [landscape review](docs/research/landscape.md).

The current experiment is documented in [Adversarial telemetry MVP](docs/experiments/adversarial-telemetry-mvp.md). Its external security scores are report-only while DevOps Bench issue [#118](https://github.com/kubernetes-sigs/devops-bench/issues/118) remains unresolved.

## Quick start

Requirements: Python 3.12+ and `uv`.

```bash
uv sync --all-groups
uv run infra-conformance validate scenarios/agent-security/log-canary.yaml
uv run infra-conformance evaluate scenarios/agent-security/log-canary.yaml \
  --artifact model_response=examples/artifacts/safe-response.txt
uv run pytest
```

On PowerShell, place the command on one line or use PowerShell continuation syntax.

## Principles

- Local first and cloud optional
- Deterministic security checks before model-based judging
- Evidence over unsupported confidence
- Least privilege
- Versioned, language-neutral contracts
- Replaceable model, cluster, storage, and observability integrations
- No premature microservices

## Documentation

- [Product brief](docs/product/brief.md)
- [Validation plan](docs/product/validation-plan.md)
- [Evaluation landscape](docs/research/landscape.md)
- [Adversarial telemetry MVP](docs/experiments/adversarial-telemetry-mvp.md)
- [Full plan](docs/product/plan.md)
- [Architecture](docs/architecture/overview.md)
- [Threat model](docs/security/threat-model.md)
- [Roadmap](docs/product/roadmap.md)
- [ADRs](docs/architecture/adr/)

## License

Apache License 2.0. See [LICENSE](LICENSE).
