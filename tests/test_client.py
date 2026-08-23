from __future__ import annotations

import json

import httpx
import pytest
from findog_client import FindogClient, FindogValidationError, ObligationLifecycle
from findog_client.generated import errors


OBLIGATION = {
    "id": "11111111-1111-1111-1111-111111111111",
    "ledger_id": "22222222-2222-2222-2222-222222222222",
    "category_id": "33333333-3333-3333-3333-333333333333",
    "category_code": "energy",
    "key": "energy-2026-08",
    "name": "Energy",
    "notes": None,
    "lifecycle": "ready",
    "period": {"year": 2026, "month": 8},
    "effective_value_source": "integration",
    "current_amount": "425.30",
    "amount_state": "confirmed",
    "amount_source": "integration",
    "issue_date": "2026-08-01",
    "issue_date_state": "confirmed",
    "issue_date_source": "integration",
    "due_date": "2026-08-20",
    "due_date_state": "confirmed",
    "due_date_source": "integration",
    "currency": "PLN",
    "paid_at": None,
    "created_at": "2026-08-01T10:00:00Z",
    "updated_at": "2026-08-01T10:00:00Z",
}


def make_client(handler: httpx.MockTransport) -> FindogClient:
    client = FindogClient(
        base_url="https://findog.example.test/",
        api_key="fdg_live_test",
    )
    client._client._httpx_args["transport"] = handler
    return client


def assert_auth(request: httpx.Request) -> None:
    assert request.headers["Authorization"] == "Bearer fdg_live_test"


def test_list_obligations_sends_filters_and_authentication() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        assert request.url.path == "/api/v1/integration/obligations"
        assert dict(request.url.params) == {
            "year": "2026",
            "month": "8",
            "category_code": "energy",
            "lifecycle": "ready",
        }
        assert_auth(request)
        return httpx.Response(200, json={"data": [OBLIGATION], "count": 1})

    with make_client(httpx.MockTransport(handler)) as client:
        result = client.obligations.list(
            year=2026,
            month=8,
            category_code="energy",
            lifecycle=ObligationLifecycle.READY,
        )

    assert result.count == 1
    assert result.data[0].key == "energy-2026-08"


def test_update_obligation_serializes_only_supplied_values() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "PATCH"
        assert request.url.path == "/api/v1/integration/obligations/energy-2026-08"
        assert_auth(request)
        assert json.loads(request.content) == {"current_amount": "450.00"}
        return httpx.Response(200, json={**OBLIGATION, "current_amount": "450.00"})

    with make_client(httpx.MockTransport(handler)) as client:
        result = client.obligations.update(
            "energy-2026-08",
            current_amount="450.00",
        )

    assert result.current_amount == "450.00"


def test_append_note_uses_append_only_endpoint() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert request.url.path == "/api/v1/integration/obligations/energy-2026-08/notes"
        assert_auth(request)
        assert json.loads(request.content) == {"text": "Imported invoice FV/123/2026"}
        return httpx.Response(
            200,
            json={**OBLIGATION, "notes": "Imported invoice FV/123/2026"},
        )

    with make_client(httpx.MockTransport(handler)) as client:
        result = client.obligations.append_note(
            "energy-2026-08",
            "Imported invoice FV/123/2026",
        )

    assert result.notes == "Imported invoice FV/123/2026"


def test_validation_response_becomes_high_level_exception() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert_auth(request)
        return httpx.Response(
            422,
            json={
                "detail": [
                    {
                        "loc": ["query", "month"],
                        "msg": "Input should be less than or equal to 12",
                        "type": "less_than_equal",
                    }
                ]
            },
        )

    with (
        make_client(httpx.MockTransport(handler)) as client,
        pytest.raises(FindogValidationError),
    ):
        client.obligations.list(month=13)


def test_undocumented_status_is_not_silently_returned_as_none() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert_auth(request)
        return httpx.Response(500, text="boom")

    with (
        make_client(httpx.MockTransport(handler)) as client,
        pytest.raises(errors.UnexpectedStatus) as exc_info,
    ):
        client.obligations.get("energy-2026-08")

    assert exc_info.value.status_code == 500
