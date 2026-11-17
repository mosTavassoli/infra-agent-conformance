# Architecture overview

```text
Scenario -> Runner -> Target Provider -> Environment
                |             |
                v             v
             Adapter -> System under test
                            |
Observers ------------------+
    |
    v
Evidence -> Evaluators -> Findings -> Reporters
```

## Stable concepts

- **Scenario:** failure, attack, ground truth, permissions, and expected behavior
- **Target provider:** local or remote execution environment
- **Adapter:** integration with the system being evaluated
- **Observer:** collection of objective behavior and telemetry
- **Evaluator:** deterministic or semantic grading
- **Reporter:** human and machine-readable output

## Initial implementation

The first implementation is a Python modular monolith. Public contracts are versioned JSON/YAML rather than Python classes so future adapters can use Go, C#, Kotlin, or another language.

Established-runner adapters are translation boundaries, not orchestration layers. The DevOps Bench
adapter converts its canonical final output and tool trajectory into the core evaluator and converts
the resulting findings back into external metric scores. DevOps Bench retains ownership of agent
execution, infrastructure lifecycle, sandboxing, and artifact capture.

## Observability

OpenTelemetry is the stable boundary. Local artifacts are sufficient for the baseline. Prometheus/Grafana and Elasticsearch/Kibana remain optional adapters.
