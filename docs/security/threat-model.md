# Initial threat model

## Protected assets

- Synthetic canaries and test configuration
- Agent and model credentials
- Test-cluster availability
- Evaluation ground truth
- Report integrity
- Maintainer and contributor environments

## Trust boundaries

- User to CLI
- CLI to target environment
- Runner to agent adapter
- Agent to tools and Kubernetes API
- Agent to model provider
- Observers to artifact storage
- Plugins and container images to host

## Initial threats

- Prompt injection through logs, annotations, issues, or tool responses
- Secret leakage to a model provider or report
- Excessive Kubernetes permissions
- Unauthorized write operations
- Command or argument injection through adapters
- Cross-namespace access
- Ground-truth exposure to the evaluated agent
- Malicious plugin images
- Report tampering
- Supply-chain compromise

## Initial controls

- Disposable, isolated environments
- Synthetic credentials only
- Runner-scoped sandbox identity with task-scoped admission making the protected fixture read-only
- Schema validation
- No shell capability added by this project; an external runner's existing shell must remain inside
  a disposable agent sandbox
- Exact canary matching across artifacts
- Separation of ground truth from agent-visible context
- Withheld security scores for unsandboxed, incomplete, or structurally malformed tool-call evidence
- Forbidden Secret access detection includes the Kubernetes short name `sec`
- Run-scoped smoke-test kubeconfig and private temporary state; failed or unverifiable teardown
  retains recovery files without publishing their contents
- Signed release artifacts in a later release milestone

## Out of scope for the foundation

- Production-cluster guarantees
- Automated remediation
- Perfect prompt-injection prevention
- Encoded or transformed canary disclosure
- Inspection of model-provider request bodies
- Complete detection of non-`kubectl` side effects
- Protection against a compromised host
