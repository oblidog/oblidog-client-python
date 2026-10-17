"""Regression coverage for error schemas with repeated inline model titles."""

import importlib
import json
import subprocess
import sys
from pathlib import Path

import httpx
import pytest


def test_generation_preserves_conflicts_with_duplicate_params_titles(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = Path(__file__).resolve().parents[1]
    spec = json.loads((root / "openapi/integration.json").read_text())
    schemas = spec["components"]["schemas"]
    params = {"type": "object", "title": "Params", "additionalProperties": True}
    schemas["ApiErrorResponse"] = {
        "type": "object",
        "properties": {"params": params},
    }
    schemas["IntegrationConflictResponse"]["properties"]["params"] = params
    schema_path = tmp_path / "integration.json"
    schema_path.write_text(json.dumps(spec))
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "openapi_python_client",
            "generate",
            "--fail-on-warning",
            "--path",
            str(schema_path),
            "--config",
            str(root / "openapi-client.yaml"),
            "--meta",
            "none",
            "--output-path",
            str(tmp_path / "regression_client"),
        ],
        capture_output=True,
        check=False,
        text=True,
        cwd=tmp_path,
        timeout=60,
    )
    assert result.returncode == 0, result.stdout + result.stderr

    monkeypatch.syspath_prepend(str(tmp_path))
    models = importlib.import_module("regression_client.models")
    params_payload = {"revision": 3}
    for name in ("ApiErrorResponse", "IntegrationConflictResponse"):
        payload = {
            "code": "integration_conflict",
            "detail": {"code": "revision_conflict"},
            "params": params_payload,
        }
        assert getattr(models, name).from_dict(payload).to_dict() == payload

    client = importlib.import_module("regression_client.client").AuthenticatedClient(
        base_url="https://example.test", token="test"
    )
    for operation in ("start", "finish"):
        endpoint = importlib.import_module(
            f"regression_client.api.integration.integration_{operation}_integration_run"
        )
        response = endpoint._parse_response(
            client=client,
            response=httpx.Response(409, json=payload),
        )
        assert isinstance(response, models.IntegrationConflictResponse)
        assert response.to_dict() == payload
