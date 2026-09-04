#!/usr/bin/env bash

set -euo pipefail

project_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
test_env="$(mktemp -d)"
trap 'rm -rf "$test_env"' EXIT

cd "$project_root"

uv sync --all-groups --locked
uv build --clear
uv run twine check --strict dist/*
uv run python scripts/verify_dist.py dist

uv venv --python 3.12 "$test_env"
uv pip install --python "$test_env/bin/python" dist/*.whl
"$test_env/bin/python" scripts/smoke_installed.py
