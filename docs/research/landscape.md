# Infrastructure-agent evaluation landscape

Last reviewed: 16 November 2026

## Purpose

This review tests whether Infrastructure Agent Conformance addresses an unmet need or would duplicate an existing benchmark. It is a point-in-time assessment, not an exhaustive catalog. Project capabilities should be verified against their current documentation before making integration decisions.

## Main finding

The general problem of evaluating Kubernetes and SRE agents is already served by several active projects. Building another cluster provisioner, agent runner, and broad reliability benchmark would add limited value.

The narrower hypothesis still worth validating is:

> Existing benchmarks may benefit from a portable, deterministic security-conformance profile covering hostile operational content, synthetic-data leakage, authorization boundaries, forbidden operations, egress, approval boundaries, and safe abstention.

This is a hypothesis, not yet a confirmed product gap.

## Closest projects

| Project | Primary emphasis | Relevant capabilities | Implication |
|---|---|---|---|
| [Kubernetes SIGs DevOps Bench](https://github.com/kubernetes-sigs/devops-bench) | Live DevOps-agent evaluation | Local `kind` and GKE targets, fault injection, agent harnesses, deterministic state verification, safeguards, catastrophic outcomes, and pluggable fault, verifier, and metric registries | Closest architectural overlap and the first upstream integration candidate |
| [SREGym](https://github.com/SREGym/SREGym) | Live SRE diagnosis and mitigation | Large incident suite, local `kind` support, isolated agent execution, diagnosis and mitigation stages, and agent/model comparison | Strong existing home for broad SRE scenarios; do not reproduce its incident catalog |
| [ITBench](https://github.com/itbench-hub/ITBench) | Enterprise IT automation | Kubernetes-based SRE, CISO, and FinOps scenarios, reference agents, deployment tooling, and leaderboards | Formal evidence that the general evaluation problem is established; published at ICML 2025 |
| [k8s-ai-bench](https://github.com/gke-labs/k8s-ai-bench) | Kubernetes task capability | Ephemeral `kind` or vCluster environments, operational tasks, repeated execution, and Pass@k-style reporting | Covers model and agent operational capability rather than a dedicated security-conformance profile |
| [Cloud-OpsBench](https://github.com/LLM4Ops/Cloud-OpsBench) | Reproducible root-cause analysis | Snapshot replay, hundreds of Kubernetes fault cases, evidence milestones, process scoring, and an MCP interface | Demonstrates a lower-cost alternative to live clusters for diagnosis evaluation |
| [infra-bench](https://github.com/kubeply/infra-bench) | Real infrastructure tasks | Kubernetes task dataset with broader infrastructure datasets planned | Additional evidence that a generic infrastructure benchmark would enter a crowded category |

## Security-specific work

### Telemetry and prompt injection

- [When AIOps Become "AI Oops"](https://arxiv.org/abs/2508.06394) analyzes adversarial manipulation of telemetry consumed by AIOps agents and proposes a telemetry-sanitization defense.
- [LogJack](https://arxiv.org/abs/2604.15368) provides a benchmark and [repository](https://github.com/HarshShah1997/logjack) for indirect prompt injection through cloud logs, including command execution, exfiltration, privilege changes, and remote-code-execution payloads.
- [AgentDojo](https://github.com/ethz-spylab/agentdojo) evaluates indirect prompt-injection attacks and defenses for general tool-using agents rather than Kubernetes operations specifically.

### Kubernetes agent containment

- [Containing the Autonomous Operator](https://arxiv.org/abs/2610.02861) defines a Kubernetes-specific threat model and defense-in-depth architecture spanning identity, RBAC, admission, sandboxing, network egress, tool mediation, secrets, runtime detection, and approval. Its evaluation is qualitative and explicitly proposes future empirical validation.
- [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026) provides a general agent-security taxonomy.
- [MITRE ATLAS](https://atlas.mitre.org/) catalogs adversarial techniques against AI-enabled systems.
- The [NIST AI Agent Standards Initiative](https://www.nist.gov/super-intelligence/si-agent-standards-initiative) is developing broader agent interoperability, identity, and security guidance.

The CNCF Kubernetes AI Conformance program is adjacent but different: it assesses whether Kubernetes platforms can run AI and machine-learning workloads. It does not certify the behavior of an AI agent operating Kubernetes infrastructure.

## DevOps Bench architecture findings

The first source review found several useful extension points:

- Tasks are typed YAML contracts with optional chaos and verification specifications.
- Verification entries distinguish objectives from safety safeguards.
- A failed catastrophic safeguard can zero the outcome.
- Faults, verifiers, and post-run metrics are registries with Python entry-point discovery through `devops_bench.faults`, `devops_bench.verifiers`, and `devops_bench.metrics`.
- Agent harnesses emit a canonical result containing final output, tool-call trajectory, token usage, latency, errors, and metadata.
- Post-run cheat detection already scans tool arguments, tool results, and final output, demonstrating that deterministic transcript inspection is feasible.
- A third-party metric can inspect the complete result and trajectory without an orchestration change. A custom metric is report-only unless it emits one of the score keys recognized by the composite outcome contract.
- Open issue [#118](https://github.com/kubernetes-sigs/devops-bench/issues/118) already proposes passing `AgentResult` into verification so transcript checks can participate directly in normal objective and safeguard semantics.

Current documented tasks and open work include security remediation, secret rotation, RBAC safeguards, sandbox hardening, and benchmark-integrity checks. During this review, no in-tree task or open pull request was found that deliberately places hostile instructions and a synthetic canary in Kubernetes telemetry, then grades whether the investigated agent follows the instruction, leaks the canary, or crosses its authorized scope.

That negative finding is provisional. It must be confirmed with maintainers before implementation. A new generic transcript extension should not be proposed independently of issue #118.

## Candidate gap

A security-conformance profile could complement existing benchmarks with deterministic assertions such as:

- A synthetic canary observed during investigation does not appear in unauthorized output or tool arguments.
- Log lines, annotations, events, tickets, and tool responses are treated as untrusted data rather than instructions.
- An agent does not attempt forbidden Kubernetes verbs or access outside permitted namespaces.
- A read-only investigation does not propose or invoke an unapproved mutation path.
- External egress and high-risk tool calls remain blocked or approval-gated.
- The final diagnosis cites observable evidence and abstains when evidence is insufficient.
- Tool calls, policy decisions, Kubernetes audit events, and final output are correlated into an auditable result.

The differentiator would be the portable profile and evidence contract, not another infrastructure runner.

## Risks to the hypothesis

- DevOps Bench may already plan to implement the same security scenarios.
- Existing generic security benchmarks may be adaptable with little additional work.
- Agent maintainers may prefer project-specific regression tests over a shared profile.
- Normalizing tool trajectories across independent agents may be too lossy for reliable policy evaluation.
- Synthetic leakage and forbidden-call checks may be useful but insufficient to influence adoption decisions.

## Current recommendation

Pause standalone cluster and agent-runner development. Validate the security-profile hypothesis through maintainer conversations and one small upstream-compatible experiment. Continue independently only if users or maintainers identify a concrete gap that cannot reasonably live in an existing project.
