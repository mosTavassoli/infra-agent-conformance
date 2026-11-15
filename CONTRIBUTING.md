# Contributing

The project is in its foundation phase. Discussion about user problems and test scenarios is as valuable as code.

## Before contributing

- Read `AGENTS.md`, the product brief, and the threat model.
- Open an issue before large architectural changes.
- Never include real credentials, production data, or confidential incident details.

## Development

```bash
uv sync --all-groups
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

## Commit expectations

- Keep changes focused.
- Add tests for behavior.
- Update contracts and documentation together.
- Explain security and compatibility implications.

Contributions will use a Developer Certificate of Origin before the first public release.
