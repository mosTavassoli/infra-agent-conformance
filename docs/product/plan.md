# Open-Source Conformance Platform Plan

**Owner:** Mostafa Tavassoli  
**Status:** Product and architecture planning  
**Last updated:** 2026-11-15  
**Project name:** Infrastructure Agent Conformance  
**Repository:** `infra-agent-conformance`

## 1. Executive decision

Build an extensible, open-source conformance platform for testing the reliability and security of infrastructure agents and distributed systems.

The first focused product will be:

> A Kubernetes AI-agent security conformance suite that runs reproducible incidents and adversarial scenarios, observes agent behavior, and produces evidence-based safety and usefulness reports.

The project must remain focused enough to release, while its contracts allow future scenario packs for APIs, Kafka, Redis/Valkey, databases, AWS, MCP agents, and non-AI distributed applications.

This direction is preferred over building another general Kubernetes troubleshooting agent or another generic AI gateway. Existing projects already cover those areas well. The proposed project should complement and test those tools rather than clone them.

## 2. Why build it

### User problem

Teams experimenting with AI infrastructure agents need objective answers to questions such as:

- Can the agent diagnose a real failure correctly?
- Does it cite evidence or invent conclusions?
- Can hostile text in logs or annotations manipulate it?
- Can it read or expose sensitive information?
- Does it attempt operations outside its authorization?
- Does it abstain when the available evidence is insufficient?
- How consistent, fast, and expensive is it across repeated runs?
- Does a model, prompt, policy, or tool upgrade introduce a regression?

### Target users

- Maintainers of AI SRE and Kubernetes-agent projects
- Platform and SRE teams evaluating infrastructure agents
- Security engineers reviewing agent permissions and data exposure
- AI engineers building MCP or LangGraph infrastructure tools
- Researchers evaluating agent safety and operational usefulness

The project does not need to be useful to everyone. It should solve an important problem for a clearly defined and growing technical audience.

## 3. Career alignment

### Staff Engineer path

The project should demonstrate more than coding:

- Problem discovery and requirement gathering
- Architecture and trade-off analysis
- Written RFCs and Architecture Decision Records (ADRs)
- Security and reliability ownership
- Versioning and migration design
- Cost awareness
- Contributor enablement and technical mentoring
- Metrics showing whether the platform helps its users

### Platform Engineer path

The platform should eventually provide:

- A self-service CLI
- Safe defaults
- Reusable scenario packs
- CI integration
- Kubernetes and Helm packaging
- Policy controls
- OpenTelemetry-based observability
- Clear upgrade and compatibility paths
- Useful reports without requiring deep knowledge of the implementation

### Founder path

The project should be used to discover a market, not assume one exists. Founder-oriented work includes:

- Interviewing maintainers and platform teams
- Releasing early and observing real usage
- Measuring repeat usage rather than GitHub stars alone
- Learning which reports or integrations users value
- Supporting users and handling operational problems
- Testing willingness to pay before building a hosted platform

Possible commercial extensions are documented later, but the open-source tool must provide genuine value by itself.

## 4. Relevance to the current role

Mostafa's current experience includes C#/.NET, backend systems, database performance, secure integrations, authentication, and integration testing. The project can strengthen directly applicable skills through a fictional, generic .NET reference workload.

The reference workload may include:

- A REST API
- PostgreSQL
- OAuth-protected service integration
- Background processing
- An external dependency
- OpenTelemetry instrumentation
- Testcontainers-based integration tests

Generic scenarios may include:

- Slow queries and database lock contention
- OAuth token endpoint failure
- Expired credentials
- External API latency or malformed responses
- Duplicate event delivery
- Retry amplification
- Partial background-job failure
- Sensitive values accidentally written to logs

### Employer and intellectual-property safeguards

- Do not copy employer code, architecture, incidents, names, data, or documentation.
- Do not reproduce confidential implementation details in scenarios or articles.
- Use personal equipment, accounts, repositories, and model credentials.
- Review the employment agreement and company open-source policy.
- Obtain approval before proposing the project's direct use inside the company.
- Present all reference systems as fictional and generally applicable.

## 5. Product boundaries

### Version 0.1 scope

- Run isolated scenarios on a local `kind` cluster.
- Support a small LangGraph reference agent.
- Support at least one external agent through an adapter.
- Observe Kubernetes API activity and agent outputs.
- Detect synthetic secret leakage and forbidden operations.
- Grade diagnosis quality, evidence grounding, and safe abstention.
- Export terminal, JSON, and JUnit reports.
- Require no cloud account and no always-running infrastructure.

### Explicit version 0.1 non-goals

- No automatic remediation of real infrastructure
- No production cluster support claim
- No custom Kubernetes operator
- No microservice architecture
- No Kafka or Redis dependency in the platform control plane
- No mandatory Elasticsearch cluster
- No complex web dashboard
- No blockchain
- No custom cryptographic algorithms
- No attempt to replace HolmesGPT, K8sGPT, Radar, or agent gateways
- No claim that prompt injection can be perfectly detected or prevented

## 6. Architecture principles

1. **Focused first use case, extensible core:** Kubernetes agent safety comes first; generic abstractions must be earned by real use cases.
2. **Language-neutral boundaries:** scenario and adapter contracts must not depend on Python classes.
3. **Local first:** the complete baseline must run without AWS or paid infrastructure.
4. **Deterministic security checks first:** use exact checks for canary leakage and forbidden operations before using an LLM judge.
5. **Evidence over confidence claims:** every conclusion should reference captured evidence.
6. **Least privilege:** test agents with explicit, minimal permissions.
7. **Observable by design:** propagate run and scenario identifiers through logs, traces, reports, and tool calls.
8. **Replaceable infrastructure:** model providers, storage, clusters, policies, and observability backends should sit behind stable contracts.
9. **No premature distribution:** begin as a modular monolith and split components only when measured requirements justify it.
10. **Cost is a product feature:** record token consumption, infrastructure use, and estimated investigation cost.

## 7. Logical architecture

```text
Scenario Pack
     |
     v
Scenario Runner ---> Target Provider ---> Isolated Environment
     |                                       |
     |                                       v
     +----------> Agent/System Adapter ---> System Under Test
                                             |
                                             v
Observers ------------------------------> Evidence Bundle
                                             |
                                             v
Evaluators -----------------------------> Findings and Scores
                                             |
                                             v
Reporters ------------------------------> CLI / JSON / JUnit / HTML
```

### Core extension points

#### Scenario

Describes:

- Environment prerequisites
- Fault or adversarial input
- Ground truth
- Expected evidence
- Allowed operations
- Forbidden operations
- Success, failure, and abstention conditions
- Cleanup procedure

Scenarios should be YAML documents validated by a versioned JSON Schema.

#### Target provider

Creates or connects to an execution environment:

- Local `kind`
- Existing Kubernetes context
- EKS later
- Docker Compose later
- Other environments only after a demonstrated need

#### Agent/system adapter

Runs a system under test:

- LangGraph reference agent
- HolmesGPT adapter
- K8sGPT adapter
- MCP-compatible agent
- .NET or JVM reference application
- Future third-party agents

#### Observer

Collects objective evidence:

- Kubernetes audit activity
- Agent tool calls
- Application and platform logs
- OpenTelemetry traces and metrics
- Network attempts where practical
- Model requests and responses with secrets removed
- Token usage, latency, and estimated cost
- Synthetic canary exposure

#### Evaluator

Evaluates:

- Root-cause correctness
- Evidence grounding
- Unsupported claims
- Secret leakage
- Prompt-injection success
- Unauthorized operation attempts
- Safe abstention
- Latency, consistency, and cost

#### Reporter

Initial outputs:

- Human-readable terminal output
- Versioned JSON
- JUnit XML

Later outputs:

- Static HTML
- SARIF or GitHub Checks
- Elasticsearch documents and Kibana dashboards
- Hosted history and comparison dashboards

## 8. Language and plugin strategy

### Initial implementation

Use Python for version 0.1 because it provides the shortest path to LangGraph, model-provider integrations, evaluation libraries, and Kubernetes automation.

Recommended initial stack:

| Concern | Initial selection |
|---|---|
| Language | Python 3.12+ |
| CLI | Typer |
| Models/configuration | Pydantic |
| Package management | `uv` |
| Scenario validation | JSON Schema |
| Kubernetes client | Official Python client |
| Local cluster | `kind` |
| Packaging | OCI containers |
| Deployments | Helm |
| Testing | pytest |
| AI workflow | LangGraph |
| AI tool protocol | MCP where appropriate |
| Telemetry | OpenTelemetry |
| Initial persistence | Artifact files plus SQLite index |
| CI | GitHub Actions |
| Documentation | MkDocs |

### Language-neutral contracts

Use:

- JSON over standard input/output for simple local plugins
- HTTP with an OpenAPI contract for remote adapters
- MCP for compatible AI tool interactions
- OCI images as the portable plugin package

Each request and result must include a schema version. Plugins should advertise capabilities so incompatible scenarios fail before execution.

Example capability categories:

- `kubernetes.read`
- `kubernetes.write`
- `mcp.tools`
- `streaming`
- `cost.reporting`
- `telemetry.otel`
- `security.redaction`

### Future language decisions

Introduce another language only when a requirement justifies its cost.

#### Go is appropriate for

- Long-running Kubernetes collectors
- Controllers or operators
- Low-memory binaries
- High-concurrency or high-throughput components
- Deep Kubernetes-native integrations

#### C#/.NET is appropriate for

- The generic reference backend
- A future adapter SDK
- Testcontainers examples
- OAuth and service-integration scenarios
- Applying knowledge relevant to the current role

#### Java/Kotlin is appropriate for

- JVM reference workloads
- Spring Boot or Quarkus integrations
- Kafka-focused examples
- Cross-runtime resilience comparisons

Do not begin with several production languages. Preserve the protocol boundaries, then add implementations when there is a user or performance reason.

## 9. Observability strategy

### Decision

Use OpenTelemetry as the vendor-neutral instrumentation layer. Add Elasticsearch and Kibana as an optional observability profile rather than a core dependency.

This preserves flexibility and allows other backends such as Grafana, Loki, Tempo, Prometheus, OpenSearch, or commercial platforms.

### Phase 1: lightweight baseline

- Structured JSON logs
- OpenTelemetry traces and metrics
- Run artifacts stored locally
- Correlation fields on every record:
  - `run_id`
  - `scenario_id`
  - `agent_id`
  - `model_id`
  - `target_id`
  - `trace_id`
- Terminal and JSON reports

No Elasticsearch is required to run the baseline.

### Phase 2: local developer observability

- OpenTelemetry Collector
- Prometheus for metrics
- Grafana for basic operational dashboards
- Optional Loki/Tempo profile if it provides a lightweight local experience

This phase validates the telemetry model before adding a heavier search backend.

### Phase 3: Elasticsearch and Kibana integration

Add an optional Docker Compose or Helm profile:

```text
Platform and agent telemetry
          |
          v
OpenTelemetry Collector
          |
          v
Elasticsearch
          |
          v
Kibana dashboards
```

Potential Elasticsearch indexes or data streams:

- Scenario runs
- Agent tool calls
- Security findings
- Evidence metadata
- Application and platform logs
- Model cost and latency measurements

Useful Kibana dashboards:

- Pass/fail trends by agent and model
- Secret-leak and policy-violation findings
- Prompt-injection attack success rate
- Root-cause and evidence-grounding scores
- Token cost and investigation duration
- Tool-call timelines for individual investigations
- Failure rates by Kubernetes or scenario version

### Elasticsearch design rules

- The core must emit OTLP and versioned result documents, not call Elasticsearch throughout the domain code.
- Keep Elasticsearch-specific mapping and publishing code in an adapter.
- Do not require Logstash initially; the OpenTelemetry Collector can handle the first telemetry pipeline.
- Define index lifecycle and retention settings before storing large logs.
- Redact credentials and unnecessary personal data before export.
- Do not index hidden model reasoning or secrets.
- Support OpenSearch later if users request an alternative.
- Document Elastic component licenses and deployment implications before distributing bundled images.

### Why Elasticsearch/Kibana should not be in version 0.1

- It increases local memory and CPU requirements.
- It adds schema, lifecycle, and operational maintenance.
- Early development needs correct evidence and evaluation semantics more than dashboards.
- A stable OpenTelemetry and result schema makes Elasticsearch easy to add later without redesigning the core.

## 10. Security model

### Primary threats

- Direct and indirect prompt injection
- Malicious instructions in logs, annotations, issues, and tool responses
- Secret or personal-data leakage to a model provider
- Excessive Kubernetes permissions
- Unauthorized write operations
- Tool argument injection
- Command injection through adapters
- Cross-namespace data access
- Poisoned long-term memory
- Untrusted plugin images
- Supply-chain compromise
- Misleading evidence and unsafe remediation recommendations

### Safety controls

- Run scenarios in isolated, disposable environments.
- Use only synthetic secrets and canary values.
- Exclude real production credentials.
- Apply least-privilege Kubernetes RBAC.
- Separate read and write identities.
- Keep the reference agent read-only initially.
- Do not expose arbitrary shell execution.
- Validate adapter inputs and outputs against schemas.
- Record authorization decisions and tool calls.
- Add human approval before any future write capability.
- Treat all collected content as untrusted data.
- Use deterministic checks for exact policy violations.
- Sign release artifacts and publish checksums.

### Supply-chain tools

- Trivy for images and dependencies
- Gitleaks for secret scanning
- Syft for SBOM generation
- Cosign for release and image signing
- Dependabot or Renovate
- OpenSSF Scorecard
- Protected release workflow

## 11. Initial scenario catalog

### Kubernetes reliability

1. CrashLoopBackOff caused by invalid configuration
2. Failed liveness or readiness probe
3. Missing ConfigMap
4. Resource exhaustion or OOM
5. DNS or Service connectivity failure

### Agent security

1. Malicious instruction embedded in an application log
2. Malicious instruction embedded in a Kubernetes annotation
3. Synthetic credential placed in logs and expected to be redacted
4. Request to inspect a forbidden namespace or Secret
5. Insufficient evidence where the correct behavior is to abstain

### Later distributed-system packs

- Kafka consumer lag
- Duplicate message delivery
- Consumer rebalance behavior
- Redis/Valkey unavailability
- Cache stampede
- Retry storms
- Database lock contention
- External API timeout
- Partial dependency failure
- Event ordering and idempotency

Kafka and Redis/Valkey are initially systems under test, not mandatory platform dependencies.

## 12. Evaluation model

### Deterministic checks

- Did a known canary appear in an outbound request, log, artifact, or final answer?
- Did the agent attempt a forbidden Kubernetes verb?
- Did it query a forbidden namespace or resource?
- Did it identify the correct resource and failure signal?
- Did it claim that an operation succeeded when it did not occur?

### Semantic checks

- Is the root cause correct?
- Does each conclusion reference relevant evidence?
- Are recommendations supported and safe?
- Did the agent appropriately communicate uncertainty?
- Did it abstain when necessary?

### Metrics

- Diagnosis accuracy
- Evidence precision and coverage
- Unsupported-claim rate
- Secret-leak rate
- Attack success rate
- Unauthorized-operation attempt rate
- Safe-abstention rate
- Time to diagnosis
- Token consumption and estimated cost
- Variance across repeated runs

Semantic evaluation may use an LLM judge, but reports must clearly distinguish deterministic facts from model-based scoring.

## 13. Open-source structure

Recommended license: **Apache License 2.0**.

Required project documents:

- README with the concrete problem and quick start
- LICENSE
- SECURITY.md
- CONTRIBUTING.md
- Code of Conduct
- Governance and maintainer expectations
- Threat model
- Architecture overview
- ADR directory
- Compatibility policy
- Versioning policy
- Changelog
- Public roadmap

Use a Developer Certificate of Origin initially instead of introducing a complex Contributor License Agreement without a business reason.

## 14. Possible repository structure

```text
/
  cli/
  core/
  contracts/
    schemas/
    openapi/
  scenarios/
    kubernetes-reliability/
    agent-security/
  adapters/
    langgraph-reference/
    external-agent/
  observers/
  evaluators/
  reporters/
  reference-workloads/
    dotnet-service/
  deploy/
    kind/
    helm/
    observability/
  docs/
    architecture/
    adr/
    threat-model/
  tests/
```

This is a planning structure, not a requirement to create every directory immediately.

## 15. Cost strategy

### Local development

| Item | Expected cost |
|---|---:|
| Python, Kubernetes, Helm, LangGraph | Free |
| Local Kafka and Redis/Valkey | Free |
| Public GitHub repository | Free under applicable public-project limits |
| Local OpenTelemetry stack | Free |
| Local Elasticsearch/Kibana | Free infrastructure cost, but consumes machine resources |
| Domain | Approximately USD 10-25/year |
| Initial model API use | Approximately USD 5-30/month with strict budgets |

### AWS guidance

- Do not require AWS for baseline development.
- Standard EKS control-plane pricing is currently USD 0.10 per cluster-hour, approximately USD 73/month before worker nodes and networking.
- An always-running small EKS environment can easily reach USD 120-250+ per month.
- Do not use MSK Serverless for early development; its base cluster charge can be hundreds of dollars per month before data usage.
- Use local Kafka or Strimzi for learning and scenarios.
- Use Bedrock only on demand and record token costs.
- Create EKS environments with OpenTofu/Terraform, run a planned test, and destroy them immediately.
- Configure AWS Budgets and billing alarms before provisioning resources.
- Review NAT Gateway, load balancer, public IPv4, cross-AZ, and log-ingestion costs before use.

## 16. Delivery phases

### Phase 0: discovery and validation — 2 to 3 weeks

- Interview at least five maintainers, platform engineers, or security engineers.
- Review open issues and evaluation systems in adjacent projects.
- Contribute or propose one relevant scenario to an established project.
- Write a one-page product brief and initial threat model.
- Confirm the first five scenarios and measurable outcomes.

**Exit condition:** At least three external people confirm that regression or security testing is a real problem, and at least one agrees to review the prototype.

### Phase 1: executable skeleton — 3 to 4 weeks

- Define versioned scenario and result schemas.
- Build the CLI and `kind` target provider.
- Implement one Kubernetes reliability scenario.
- Implement the LangGraph reference adapter.
- Capture structured artifacts and OpenTelemetry identifiers.
- Produce terminal and JSON output.

**Exit condition:** A new local run can create a cluster, execute a scenario, report a result, and clean up reliably.

### Phase 2: security baseline — 4 to 6 weeks

- Add synthetic canary generation and detection.
- Capture Kubernetes API activity.
- Add forbidden-operation and namespace-access checks.
- Add malicious log and annotation scenarios.
- Add safe-abstention evaluation.
- Add JUnit output and CI execution.

**Exit condition:** The framework deterministically detects all intentionally seeded canary leaks and forbidden actions in its own test fixtures.

### Phase 3: external integration — 3 to 5 weeks

- Add one external AI SRE agent adapter.
- Run scenarios repeatedly against at least two model configurations.
- Record latency, token use, and estimated cost.
- Publish an honest report including failures and limitations.

**Exit condition:** An external maintainer can reproduce the results and provide actionable feedback.

### Phase 4: current-role and distributed-system packs — 4 to 8 weeks

- Add the generic .NET reference workload.
- Add Testcontainers examples.
- Add PostgreSQL, OAuth, external dependency, and retry scenarios.
- Add one Kafka scenario and one Redis/Valkey scenario.
- Document the distributed-system behavior being tested.

**Exit condition:** Scenarios demonstrate real failure semantics rather than merely checking whether a container is running.

### Phase 5: observability backends — 3 to 5 weeks

- Validate the OpenTelemetry semantic model.
- Add a lightweight Prometheus/Grafana profile.
- Add optional Elasticsearch publishing.
- Add initial Kibana dashboards.
- Define retention, redaction, and index lifecycle behavior.

**Exit condition:** The same run can use no backend, the lightweight backend, or Elasticsearch/Kibana without changing scenario or evaluator code.

### Phase 6: AWS and multi-environment execution — only after demand

- Add an EKS target provider.
- Add workload identity and KMS examples.
- Add Bedrock model support.
- Add ephemeral infrastructure automation.
- Test cost and cleanup safeguards.

**Exit condition:** A complete cloud run can be created and destroyed reproducibly with an explicit cost estimate.

### Phase 7: hosted product exploration — only after repeated usage

- Result history
- Team comparisons
- Scheduled execution
- Private runners
- Enterprise policy packs
- Support and security assessments

Do not begin this phase based only on GitHub stars or social-media interest.

## 17. Version 0.1 acceptance criteria

- A new user can install and run the baseline in under 15 minutes on a documented machine configuration.
- No cloud account is required.
- The tool creates and destroys an isolated `kind` environment.
- At least five scenarios are reproducible.
- One LangGraph agent and one external agent are supported.
- All synthetic canary leaks created by the fixtures are detected.
- Forbidden Kubernetes API attempts are detected.
- Reports distinguish deterministic and model-judged findings.
- JSON and JUnit outputs are versioned and documented.
- Latency and model cost are recorded.
- OpenTelemetry correlation works across a run.
- Kafka, Redis, Elasticsearch, and a database are not mandatory platform dependencies.
- A threat model, security policy, and contribution guide are published.
- At least five external developers review the project, and at least one runs it independently.

## 18. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Crowded AI SRE market | Focus on security conformance and interoperability, not another agent |
| Project becomes a technology showcase | Require every dependency to solve a documented user problem |
| Excessive abstraction | Add extension points only for observed variation; keep v0.1 a modular monolith |
| Non-deterministic model behavior | Repeat runs, report variance, and prioritize deterministic checks |
| Benchmark gaming | Isolate agents from ground truth and maintain hidden validation scenarios later |
| High LLM costs | Budgets, cheaper baseline models, caching where valid, and cost reports |
| High local resource usage | Minimal default profile; heavy observability and Kafka profiles remain optional |
| Security test code is misused | Keep scenarios isolated, synthetic, documented, and non-production by default |
| No external adoption | Validate early, integrate with existing communities, and stop or pivot at decision gates |
| Employer IP conflict | Maintain strict separation and review applicable policies |
| Solo-maintainer burnout | Small release scope, clear governance, automation, and contributor-friendly tasks |

## 19. Decision gates

### Gate A: before building beyond the prototype

Continue only if:

- The first five scenarios are clearly measurable.
- External reviewers confirm the problem is relevant.
- The local workflow is affordable and technically practical.

### Gate B: before adding Elasticsearch/Kibana

Continue only if:

- Users need historical search, investigation timelines, or comparative dashboards.
- The telemetry schema is stable enough to index.
- The optional profile can be run and removed cleanly.

### Gate C: before adding Kafka to the platform itself

Continue only if:

- Runs must be distributed across workers.
- A single-process queue is measurably insufficient.
- Delivery, ordering, replay, and backpressure requirements are documented.

### Gate D: before building a hosted service

Continue only if:

- Users repeatedly run the tool.
- Teams request shared history, private runners, or scheduled tests.
- At least several potential customers agree to a pricing or pilot conversation.

## 20. Technical writing opportunities

The project can provide content for the personal website:

- Designing language-neutral plugin contracts
- Why Kubernetes read-only access is not automatically safe
- Testing indirect prompt injection through logs
- Building deterministic safety checks for AI agents
- Evaluating safe abstention
- Failure injection without building a playground
- Kafka consumer lag and idempotency scenarios
- Redis failure modes in distributed applications
- OpenTelemetry correlation across agent investigations
- Adding Elasticsearch/Kibana without vendor-locking the core
- Lessons from CKAD applied to an open-source platform
- Running ephemeral EKS tests without an expensive monthly bill
- Architecture decisions that changed after user feedback

## 21. Immediate next planning actions

1. Select a temporary project codename only after checking existing repositories and trademarks.
2. Write the one-page product brief.
3. Define the version 0.1 scenario and result schemas on paper.
4. Select the first three reliability and two security scenarios.
5. Identify five maintainers or platform engineers for discovery conversations.
6. Choose the first external agent integration candidate.
7. Define the local machine resource budget.
8. Define a monthly model API budget.
9. Review employer open-source and IP policies.
10. Create a six-week prototype backlog only after these decisions are complete.

## 22. Final recommendation

Proceed step by step with a focused Kubernetes AI-agent security suite built on an extensible conformance core.

- Use Python for the first implementation.
- Keep contracts language-neutral.
- Use a generic .NET workload to connect learning to the current role.
- Use OpenTelemetry from the beginning.
- Add Elasticsearch and Kibana later as an optional, evidence-driven observability adapter.
- Treat Kafka, Redis/Valkey, AWS, and additional languages as deliberate later capabilities, not initial checklist items.
- Validate with real users before investing in a hosted business.

This approach provides strong technical depth for a future Staff Engineer, practical platform-engineering experience, and a credible path for discovering a future business without overengineering the first release.
