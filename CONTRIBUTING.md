# Contributing

## Branching

`main` is the only long-lived branch and should stay releasable.

Create short-lived branches for all changes, for example:

- `feat/...` for features
- `fix/...` for fixes
- `chore/...` for maintenance
- `bot/update-from-ledger-vX.Y.Z` for generated client updates

All changes should reach `main` through pull requests.

## Generated code

`src/findog_client/generated/` is generated from the Findog Ledger integration OpenAPI contract. Do not edit files in that directory by hand.

The source snapshot used for generation lives in `openapi/integration.json`.

## Local checks

Run before opening a pull request:

```bash
uv sync --all-groups
uv run ruff check src tests
uv run ruff format --check src tests
uv run pytest -q
python -m compileall -q src/findog_client
uv build
```

Generated code is excluded from handwritten Ruff checks and is instead validated by compilation and package build.
