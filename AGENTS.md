# AGENTS.md

Guidance for automated coding agents working in this repository.

## Generated code

- Do not edit files under `src/oblidog_client/generated/` by hand.
- Generated code comes from the OpenAPI specification and may be replaced during regeneration.
- Add stable behavior in the hand-written high-level client/facade instead of patching generated endpoint functions.

## Public API

- Treat symbols exported from `oblidog_client.__all__` as the supported public API.
- When adding or removing a public symbol, update:
  - `src/oblidog_client/__init__.py`
  - `tests/test_package.py`
  - the relevant `docs/reference/*.md` page
  - public docstrings used by `mkdocstrings`
- Application code and integrations should import from `oblidog_client`, not from `oblidog_client.generated`.

## Documentation

- Reference documentation is generated with `mkdocstrings`; public classes, methods, exceptions, and configuration objects must have useful docstrings.
- Keep conceptual or usage guidance in `docs/`, but keep API details close to the code in docstrings.
- If behavior exposed to users changes, update both the docs page and the relevant docstring when needed.

## Error handling and transport behavior

- Do not leak low-level `httpx` or generated-client exceptions through the high-level API when a stable Oblidog exception is appropriate.
- Preserve the original exception as `__cause__` when translating transport failures.
- Automatic retries must be bounded and limited to operations that are safe to replay.
- Do not automatically retry mutating requests unless an explicit idempotency mechanism makes replay safe.

## Validation before finishing

Run the same checks expected by CI:

```bash
uv run ruff check src tests scripts
uv run ruff format --check src tests scripts
uv run pytest -q
uv run mkdocs build --strict
python -m compileall -q src
```

If a change affects packaging or exports, also verify the built distribution and installed public API as defined by the CI workflow.
