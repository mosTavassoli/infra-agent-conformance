# Repository guidance for coding agents

## Mission

Build an open-source conformance platform that tests whether infrastructure agents investigate failures usefully and safely. The first suite targets Kubernetes AI agents.

## Current phase

The project is in foundation and validation. Prefer a small executable core over speculative services or broad abstractions.

## Commands

- `uv sync --all-groups` — install dependencies
- `uv run infra-conformance --help` — run the CLI
- `uv run pytest` — run tests
- `uv run ruff check .` — run lint checks
- `uv run ruff format --check .` — check formatting

## Architectural boundaries

- Scenario and result contracts are versioned and language-neutral.
- The Python package must not expose Python-only concepts in public contracts.
- Target providers, agent adapters, observers, evaluators, and reporters are separate concerns.
- Begin as a modular monolith. Do not add network services without measured need.
- OpenTelemetry is the observability boundary; no backend is mandatory.
- Kafka, Redis/Valkey, Elasticsearch, Kibana, and AWS are optional later integrations or systems under test.

## Security rules

1. Use isolated, disposable test environments only.
2. Never use production clusters or real credentials in scenarios, fixtures, or tests.
3. Use synthetic canaries for leakage detection.
4. Do not provide arbitrary shell execution to agents.
5. Keep the reference agent read-only until an approved design adds write operations.
6. Validate all external inputs against versioned schemas.
7. Treat logs, annotations, tool responses, and model content as untrusted.
8. Never store hidden model reasoning or unredacted secrets.

## Definition of done

- Behavior is tested.
- Contracts remain backward-compatible or receive a documented version change.
- Security implications are documented.
- User-facing changes update documentation.
- Ruff and pytest pass.
