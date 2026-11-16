# Roadmap

## Validation before further implementation

- Compare existing Kubernetes and SRE-agent benchmarks
- Confirm the security-conformance gap with maintainers and prospective users
- Test whether one adversarial-telemetry scenario fits an established runner
- Decide whether to contribute upstream, maintain a portable profile, continue independently, or stop

Standalone cluster orchestration and agent-runner development are paused until this validation is complete. See the [validation plan](validation-plan.md) and [landscape review](../research/landscape.md).

## Foundation

- Versioned scenario and result schemas
- CLI validation
- Deterministic canary leakage checks
- Product, architecture, and threat-model documentation

## Conditional local execution

- `kind` target provider
- One Kubernetes reliability scenario
- LangGraph reference adapter
- Structured artifact bundle

Implement these capabilities independently only if validation shows they cannot reasonably reuse an established benchmark.

## Security baseline

- Kubernetes API activity observation
- Forbidden operation and namespace checks
- Malicious log and annotation scenarios
- Safe-abstention evaluation
- JUnit reports

## External validation

- One external agent adapter
- Repeated model runs
- Latency, token, and cost reporting
- Public results with limitations

## Later, only after demand

- .NET reference workload
- Kafka and Redis/Valkey scenario packs
- Prometheus/Grafana profile
- Elasticsearch/Kibana adapter
- Ephemeral EKS target provider
- Hosted team features
