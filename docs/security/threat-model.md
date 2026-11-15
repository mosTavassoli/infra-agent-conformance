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
- Least-privilege read-only identity
- Schema validation
- No arbitrary shell tool for agents
- Exact canary matching across artifacts
- Separation of ground truth from agent-visible context
- Signed release artifacts in a later release milestone

## Out of scope for the foundation

- Production-cluster guarantees
- Automated remediation
- Perfect prompt-injection prevention
- Protection against a compromised host
