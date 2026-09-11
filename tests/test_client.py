from __future__ import annotations

import datetime
import json

import httpx
import pytest

from oblidog_client import (
    OblidogApiError,
    OblidogClient,
    OblidogValidationError,
    ObligationLifecycle,
)
from oblidog_client.generated import errors

OBLIGATION = {
    "id": "11111111-1111-1111-1111-111111111111",
    "ledger_id": "22222222-2222-2222-2222-222222222222",
    "category_id": "33333333-3333-3333-3333-333333333333",
    "category_code": "ENRG",
    "counterparty": None,
    "counterparty_id": None,
    "key": "ENRG-2026-08",
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

CATEGORY_RECORD = {
    "id": "44444444-4444-4444-4444-444444444444",
    "observed_at": "2026-08-01T10:00:00+00:00",
    "data": {"meter_reading_kwh": 1234.5},
    "source": "utility-import",
    "external_id": None,
    "schema_version": 1,
    "created_at": "2026-08-01T10:01:00+00:00",
}

COMPONENT = {
    "id": "55555555-5555-5555-5555-555555555555",
    "obligation_id": OBLIGATION["id"],
    "type": "principal",
    "label": "August electricity",
    "amount": "425.30",
    "source": None,
    "external_id": None,
    "metadata": {"invoice_number": "FV/123/2026"},
    "created_at": "2026-08-01T10:00:00+00:00",
    "updated_at": "2026-08-01T10:00:00+00:00",
}


def make_client(handler: httpx.MockTransport) -> OblidogClient:
    client = OblidogClient(
        base_url="https://oblidog.example.test/",
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
            "lifecycle": "ready",
        }
        assert_auth(request)
        return httpx.Response(200, json={"data": [OBLIGATION], "count": 1})

    with make_client(httpx.MockTransport(handler)) as client:
        result = client.obligations.list(
            year=2026,
            month=8,
            lifecycle=ObligationLifecycle.READY,
        )

    assert result.count == 1
    assert result.data[0].key == "ENRG-2026-08"


def test_update_obligation_serializes_only_supplied_values() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "PATCH"
        assert request.url.path == "/api/v1/integration/obligations/ENRG-2026-08"
        assert_auth(request)
        assert json.loads(request.content) == {"current_amount": "450.00"}
        return httpx.Response(200, json={**OBLIGATION, "current_amount": "450.00"})

    with make_client(httpx.MockTransport(handler)) as client:
        result = client.obligations.update(
            "ENRG-2026-08",
            current_amount="450.00",
        )

    assert result.current_amount == "450.00"


def test_append_note_uses_append_only_endpoint() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert request.url.path == "/api/v1/integration/obligations/ENRG-2026-08/notes"
        assert_auth(request)
        assert json.loads(request.content) == {"text": "Imported invoice FV/123/2026"}
        return httpx.Response(
            200,
            json={**OBLIGATION, "notes": "Imported invoice FV/123/2026"},
        )

    with make_client(httpx.MockTransport(handler)) as client:
        result = client.obligations.append_note(
            "ENRG-2026-08",
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
        pytest.raises(OblidogValidationError),
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
        client.obligations.get("ENRG-2026-08")

    assert exc_info.value.status_code == 500


def test_category_data_schema_and_list_send_expected_requests() -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        assert_auth(request)
        if request.url.path.endswith("/schema"):
            return httpx.Response(
                200,
                json={
                    "version": 1,
                    "is_active": True,
                    "schema": {"type": "object"},
                    "created_at": "2026-08-01T10:00:00+00:00",
                },
            )
        return httpx.Response(200, json={"data": [CATEGORY_RECORD], "count": 1})

    with make_client(httpx.MockTransport(handler)) as client:
        schema = client.category_data.schema()
        records = client.category_data.list(
            from_=datetime.datetime(2026, 8, 1, tzinfo=datetime.UTC),
            to=datetime.datetime(2026, 8, 2, tzinfo=datetime.UTC),
            limit=5,
            offset=2,
        )

    assert schema.version == 1
    assert records.data[0].data.to_dict() == {"meter_reading_kwh": 1234.5}
    assert requests[0].url.path == "/api/v1/integration/category/schema"
    assert dict(requests[1].url.params) == {
        "from": "2026-08-01T00:00:00+00:00",
        "to": "2026-08-02T00:00:00+00:00",
        "limit": "5",
        "offset": "2",
    }


def test_category_data_create_wraps_dict_and_preserves_explicit_none() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert request.url.path == "/api/v1/integration/category/data-records"
        assert json.loads(request.content) == {
            "observed_at": "2026-08-01T10:00:00+00:00",
            "data": {"meter_reading_kwh": 1234.5},
        }
        return httpx.Response(200, json=CATEGORY_RECORD)

    with make_client(httpx.MockTransport(handler)) as client:
        record = client.category_data.create(
            observed_at=datetime.datetime(2026, 8, 1, 10, tzinfo=datetime.UTC),
            data={"meter_reading_kwh": 1234.5},
        )

    assert record.schema_version == 1


def test_category_data_latest_validation_becomes_high_level_exception() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(422, json={"detail": []})

    with (
        make_client(httpx.MockTransport(handler)) as client,
        pytest.raises(errors.UnexpectedStatus),
    ):
        client.category_data.latest()


def test_obligation_components_use_dict_metadata_and_optional_values() -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        assert_auth(request)
        if request.method == "GET":
            return httpx.Response(200, json={"data": [COMPONENT], "count": 1})
        assert json.loads(request.content) == {
            "type": "principal",
            "label": "August electricity",
            "amount": None,
            "metadata": {"invoice_number": "FV/123/2026"},
            "external_id": "invoice-line-123",
        }
        return httpx.Response(200, json=COMPONENT)

    with make_client(httpx.MockTransport(handler)) as client:
        components = client.obligations.list_components("ENRG-2026-08")
        component = client.obligations.upsert_component(
            "ENRG-2026-08",
            type="principal",
            label="August electricity",
            external_id="invoice-line-123",
            amount=None,
            metadata={"invoice_number": "FV/123/2026"},
        )

    assert components.count == 1
    assert component.metadata.to_dict() == {"invoice_number": "FV/123/2026"}
    assert requests[0].url.path.endswith("/components")
    assert requests[1].url.path.endswith("/components/upsert")


def test_missing_parsed_response_becomes_api_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, text="boom")

    with make_client(httpx.MockTransport(handler)) as client:
        client._client.raise_on_unexpected_status = False
        with pytest.raises(OblidogApiError) as exc_info:
            client.category_data.latest()

    assert exc_info.value.status_code == 0


INTEGRATION = {
    "id": "55555555-5555-5555-5555-555555555555",
    "ledger_id": OBLIGATION["ledger_id"],
    "name": "Phone",
    "category_id": "33333333-3333-3333-3333-333333333333",
    "credentials": [],
    "enabled": True,
    "created_at": "2026-09-08T09:00:00Z",
    "updated_at": "2026-09-08T09:00:00Z",
    "enabled_at": "2026-09-08T09:00:00Z",
    "stale_after_seconds": 93600,
    "run_timeout_seconds": 1800,
    "revision": 0,
    "current_run_id": None,
    "current_started_at": None,
    "current_deadline_at": None,
    "current_finished_at": None,
    "last_finished_at": None,
    "last_result": None,
    "last_changes_detected": None,
    "last_error_code": None,
    "last_error_message": None,
    "last_success_at": None,
    "execution_state": "never_run",
    "is_stale": False,
    "health": "never_run",
}


def test_integration_context_and_start_use_shared_auth_and_caller_run_identity() -> (
    None
):
    import uuid

    run_id = uuid.uuid4()
    requests = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        assert_auth(request)
        if request.method == "GET":
            assert request.url.path == "/api/v1/integration/context"
            return httpx.Response(200, json={"integration_id": INTEGRATION["id"]})
        assert request.url.path == "/api/v1/integration/runs/start"
        assert json.loads(request.content) == {
            "run_id": str(run_id),
            "expected_revision": 0,
        }
        return httpx.Response(
            200,
            json={
                **INTEGRATION,
                "current_run_id": str(run_id),
                "current_started_at": "2026-09-08T09:00:00Z",
                "current_deadline_at": "2026-09-08T09:30:00Z",
                "revision": 1,
                "execution_state": "running",
                "health": "running",
            },
        )

    with make_client(httpx.MockTransport(handler)) as client:
        context = client.integrations.context()
        assert context["integration_id"] == INTEGRATION["id"]
        for _ in range(2):
            started = client.integrations.start(run_id=run_id, expected_revision=0)
            assert started.current_run_id == run_id
            assert started.revision == 1
            assert started.current_deadline_at == datetime.datetime(
                2026, 9, 8, 9, 30, tzinfo=datetime.UTC
            )
    assert len(requests) == 3
    assert requests[1].content == requests[2].content


def test_integration_run_fetches_context_then_starts_and_finishes() -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        assert_auth(request)
        if request.url.path == "/api/v1/integration/context":
            return httpx.Response(
                200,
                json={
                    "integration": {"revision": 4},
                    "provider": "nju",
                },
            )
        body = json.loads(request.content)
        if request.url.path == "/api/v1/integration/runs/start":
            assert body["expected_revision"] == 4
            return httpx.Response(200, json={**INTEGRATION, "revision": 5})
        assert request.url.path == "/api/v1/integration/runs/finish"
        assert body == {
            "run_id": body["run_id"],
            "result": "success",
            "changes_detected": False,
            "error": None,
        }
        return httpx.Response(200, json={**INTEGRATION, "revision": 6})

    with (
        make_client(httpx.MockTransport(handler)) as client,
        client.integrations.run() as run,
    ):
        assert run.context["provider"] == "nju"
        finished = run.finish_success(changes_detected=False)

    assert finished.revision == 6
    assert [request.url.path for request in requests] == [
        "/api/v1/integration/context",
        "/api/v1/integration/runs/start",
        "/api/v1/integration/runs/finish",
    ]


@pytest.mark.parametrize(
    ("context", "error"),
    [
        ({}, "integration context must contain an 'integration' object"),
        (
            {"integration": {}},
            "integration context integration.revision must be an integer",
        ),
        (
            {"integration": {"revision": "4"}},
            "integration context integration.revision must be an integer",
        ),
        (
            {"integration": {"revision": True}},
            "integration context integration.revision must be an integer",
        ),
    ],
)
def test_integration_run_rejects_invalid_nested_context(
    context: dict[str, object], error: str
) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert_auth(request)
        assert request.url.path == "/api/v1/integration/context"
        return httpx.Response(200, json=context)

    with (
        make_client(httpx.MockTransport(handler)) as client,
        pytest.raises(TypeError, match=error),
    ):
        client.integrations.run()


@pytest.mark.parametrize("changes", [True, False, None])
def test_integration_success_preserves_nullable_change_signal(
    changes: bool | None,
) -> None:
    import uuid

    from oblidog_client import IntegrationResult

    run_id = uuid.uuid4()

    def handler(request: httpx.Request) -> httpx.Response:
        assert_auth(request)
        assert request.method == "POST"
        assert request.url.path == "/api/v1/integration/runs/finish"
        assert json.loads(request.content) == {
            "run_id": str(run_id),
            "result": "success",
            "changes_detected": changes,
            "error": None,
        }
        return httpx.Response(
            200,
            json={
                **INTEGRATION,
                "last_result": "success",
                "last_changes_detected": changes,
                "health": "healthy",
                "execution_state": "finished",
            },
        )

    with make_client(httpx.MockTransport(handler)) as client:
        result = client.integrations.finish(
            run_id=run_id,
            result=IntegrationResult.SUCCESS,
            changes_detected=changes,
        )
        assert result.last_changes_detected is changes


def test_integration_failure_sends_sanitized_error() -> None:
    import uuid

    from oblidog_client import IntegrationResult, IntegrationRunError

    run_id = uuid.uuid4()

    def handler(request: httpx.Request) -> httpx.Response:
        assert_auth(request)
        assert json.loads(request.content) == {
            "run_id": str(run_id),
            "result": "failure",
            "changes_detected": None,
            "error": {"code": "provider_failed", "message": "Provider unavailable"},
        }
        return httpx.Response(
            200,
            json={
                **INTEGRATION,
                "last_result": "failure",
                "last_error_code": "provider_failed",
                "last_error_message": "Provider unavailable",
                "health": "error",
                "execution_state": "finished",
            },
        )

    with make_client(httpx.MockTransport(handler)) as client:
        result = client.integrations.finish(
            run_id=run_id,
            result=IntegrationResult.FAILURE,
            error=IntegrationRunError(
                code="provider_failed", message="Provider unavailable"
            ),
        )
        assert result.last_result == IntegrationResult.FAILURE


@pytest.mark.parametrize("status", [401, 403, 404, 500])
def test_integration_reporting_propagates_errors_without_retry(status: int) -> None:
    import uuid

    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        assert_auth(request)
        return httpx.Response(status, json={"detail": {"code": "revision_conflict"}})

    with make_client(httpx.MockTransport(handler)) as client:
        with pytest.raises(errors.UnexpectedStatus) as exc:
            client.integrations.start(run_id=uuid.uuid4(), expected_revision=0)
        assert exc.value.status_code == status
    assert calls == 1


def test_integration_validation_error_is_public_exception() -> None:
    import uuid

    def handler(request: httpx.Request) -> httpx.Response:
        assert_auth(request)
        return httpx.Response(
            422,
            json={
                "detail": [
                    {"loc": ["body", "run_id"], "msg": "invalid", "type": "value_error"}
                ]
            },
        )

    with (
        make_client(httpx.MockTransport(handler)) as client,
        pytest.raises(OblidogValidationError),
    ):
        client.integrations.start(run_id=uuid.uuid4(), expected_revision=0)


@pytest.mark.parametrize(
    "code",
    [
        "duplicate_key",
        "revision_conflict",
        "integration_disabled",
        "run_in_progress",
        "run_conflict",
    ],
)
@pytest.mark.parametrize("operation", ["start", "finish"])
def test_integration_conflict_is_typed_exception_without_retry(
    code: str, operation: str
) -> None:
    import uuid

    from oblidog_client import (
        IntegrationConflictCode,
        IntegrationResult,
        OblidogConflictError,
    )

    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        assert_auth(request)
        assert request.url.path.endswith("/" + operation)
        return httpx.Response(409, json={"detail": {"code": code}})

    with make_client(httpx.MockTransport(handler)) as client:
        with pytest.raises(OblidogConflictError) as exc:
            if operation == "start":
                client.integrations.start(run_id=uuid.uuid4(), expected_revision=0)
            else:
                client.integrations.finish(
                    run_id=uuid.uuid4(),
                    result=IntegrationResult.SUCCESS,
                    changes_detected=False,
                )
        assert isinstance(exc.value, OblidogApiError)
        assert exc.value.status_code == 409
        assert exc.value.code is IntegrationConflictCode(code)
        assert json.loads(exc.value.content) == {"detail": {"code": code}}
    assert calls == 1


def test_low_level_client_parses_documented_conflict() -> None:
    import uuid

    from oblidog_client import IntegrationConflictCode
    from oblidog_client.generated.api.integration import (
        integration_start_integration_run,
    )
    from oblidog_client.generated.models.integration_conflict_response import (
        IntegrationConflictResponse,
    )
    from oblidog_client.generated.models.integration_run_start import (
        IntegrationRunStart,
    )

    def handler(request: httpx.Request) -> httpx.Response:
        assert_auth(request)
        return httpx.Response(409, json={"detail": {"code": "revision_conflict"}})

    with make_client(httpx.MockTransport(handler)) as client:
        response = integration_start_integration_run.sync_detailed(
            client=client._client,
            body=IntegrationRunStart(run_id=uuid.uuid4(), expected_revision=0),
        )
        assert response.status_code == 409
        assert isinstance(response.parsed, IntegrationConflictResponse)
        assert response.parsed.detail.code is IntegrationConflictCode.REVISION_CONFLICT
