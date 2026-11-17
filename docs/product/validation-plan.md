# Validation plan

## Decision to make

Choose one of four outcomes before expanding implementation:

1. Contribute security scenarios and verifiers directly to an established benchmark.
2. Maintain a portable security-conformance pack with adapters for established benchmarks.
3. Continue as a standalone project because a validated requirement cannot fit upstream.
4. Stop or archive the experiment because existing projects solve the need sufficiently.

The default is not to build a standalone orchestration platform.

## Working hypothesis

Maintainers and platform/security teams need repeatable, deterministic evidence that infrastructure agents respect data, authorization, and action boundaries while investigating hostile or ambiguous operational content.

## Questions to answer

### Existing capability

- Which projects already test prompt injection through logs, events, annotations, tickets, or tool responses?
- Which projects inspect final output and tool trajectories for synthetic-data leakage?
- Which projects observe attempted as well as successful forbidden operations?
- Can their task and result contracts express security invariants without an LLM judge?

### User value

- Would a failed security-conformance check block an agent pilot or deployment?
- Which evidence is required: tool traces, Kubernetes audit events, policy decisions, final output, or all four?
- Do teams need a shared profile, or are project-specific tests sufficient?
- Would maintainers run these checks after model, prompt, tool, or policy changes?

### Integration

- Can the scenario be implemented as a normal DevOps Bench task?
- Can a deterministic transcript policy remain a report-only metric, or must it participate in objective and catastrophic-safeguard scoring?
- Can the same scenario semantics be represented in SREGym or another runner?
- Which result fields are sufficiently stable to remain runner-neutral?

## Validation sequence

### Stage 1: source review

- Maintain the [landscape review](../research/landscape.md).
- Inspect DevOps Bench task, fault, verifier, agent-result, and reporting contracts.
- Inspect SREGym and LogJack for reusable scenario and attack definitions.
- Record confirmed capability, missing capability, and uncertainty separately.

**Exit condition:** A documented candidate gap and at least one plausible upstream extension path.

### Stage 2: maintainer discovery

Ask DevOps Bench maintainers:

1. Is adversarial telemetry within the intended task scope?
2. Would a deterministic synthetic-canary and forbidden-action check be useful?
3. Is the existing metric extension sufficient, or should this use case join transcript-aware verifier issue [#118](https://github.com/kubernetes-sigs/devops-bench/issues/118)?
4. Which existing issue or design discussion should the scenario join?
5. What is the smallest acceptable contribution for proving it?

Ask SREGym or agent maintainers whether this evidence would affect their regression testing or release process.

**Exit condition:** At least two substantive responses, including one benchmark or agent maintainer. Silence is not treated as validation.

### Stage 3: one bounded experiment

Prototype one scenario, preferably against DevOps Bench:

**Implemented; external validation pending:** The
[adversarial telemetry MVP](../experiments/adversarial-telemetry-mvp.md) implements this stage as an
external DevOps Bench task and deterministic metric. No second scenario will be added before the
exit condition is evaluated.

1. Deploy a small workload to an isolated local cluster.
2. Place a clearly synthetic canary and hostile operational instruction in logs or an annotation.
3. Give the agent only the access required for investigation.
4. Capture final output, tool calls, policy denials, and available Kubernetes audit evidence.
5. Deterministically report:
   - canary exposure,
   - instruction following,
   - attempted forbidden calls,
   - cross-namespace access,
   - unsupported diagnosis, and
   - safe abstention.
6. Use intercepted or policy-denied actions; do not execute destructive payloads.

The experiment should reuse an existing runner. It must not introduce a new cluster lifecycle, model client, leaderboard, or reporting system.

**Exit condition:** One repeatable run demonstrates either a meaningful missing check or that the existing benchmark already handles the requirement.

## Initial technical finding

DevOps Bench already exposes plugin registries for cluster-state verifiers, chaos faults, and post-run metrics. Its agent result normalizes final output and tool trajectories, while its cheat detector scans those surfaces after a run. A third-party deterministic metric can therefore inspect canary exposure without a new extension point.

A normal verifier does not currently receive the agent result, and a custom metric does not automatically become a task safeguard or catastrophic outcome gate. Existing issue [#118](https://github.com/kubernetes-sigs/devops-bench/issues/118) covers this exact data-flow limitation. The first outreach should add a concrete security use case to that discussion or ask maintainers whether the metric path is sufficient; it should not propose another overlapping extension point.

## Evidence required to continue

Continue the security-conformance work only when all of the following hold:

- An existing benchmark does not already provide the required check.
- At least one maintainer or prospective user confirms the check is useful.
- The first scenario has deterministic pass/fail conditions.
- The work can reuse an established runner or demonstrates why that is impossible.
- The result would affect a real decision, regression gate, or security review.

## Stop conditions

Stop or archive the standalone effort if:

- the candidate scenarios fit an existing project without a separate package,
- maintainers and prospective users do not consider the evidence useful,
- reliable evaluation requires subjective judging without reproducible ground truth, or
- maintaining cross-agent adapters becomes the project rather than security evaluation.

## Deliverables

- A maintained landscape comparison
- Notes or links from maintainer discovery
- A written decision: upstream contribution, portable pack, standalone continuation, or stop
- At most one bounded proof of concept before that decision
