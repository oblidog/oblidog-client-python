from __future__ import annotations

import httpx
import pytest

from oblidog_client import OblidogConnectionError, RetryPolicy
from oblidog_client.resilience import ResilientTransport


def request(method: str = "GET") -> httpx.Request:
    return httpx.Request(method, "https://oblidog.example.test/api/v1/test")


def test_retries_transient_connection_failure_then_succeeds() -> None:
    attempts = 0

    def handler(req: httpx.Request) -> httpx.Response:
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            raise httpx.ConnectError("temporary failure", request=req)
        return httpx.Response(200, request=req)

    sleeps: list[float] = []
    transport = ResilientTransport(
        policy=RetryPolicy(max_attempts=3, initial_delay=0.5, jitter=0),
        transport=httpx.MockTransport(handler),
        sleep=sleeps.append,
    )

    response = transport.handle_request(request())

    assert response.status_code == 200
    assert attempts == 2
    assert sleeps == [0.5]


def test_retries_retryable_gateway_response() -> None:
    attempts = 0

    def handler(req: httpx.Request) -> httpx.Response:
        nonlocal attempts
        attempts += 1
        return httpx.Response(503 if attempts == 1 else 200, request=req)

    transport = ResilientTransport(
        policy=RetryPolicy(max_attempts=2, initial_delay=0, jitter=0),
        transport=httpx.MockTransport(handler),
        sleep=lambda _: None,
    )

    assert transport.handle_request(request()).status_code == 200
    assert attempts == 2


def test_gateway_exhaustion_raises_public_connection_error() -> None:
    attempts = 0

    def handler(req: httpx.Request) -> httpx.Response:
        nonlocal attempts
        attempts += 1
        return httpx.Response(503, request=req)

    transport = ResilientTransport(
        policy=RetryPolicy(max_attempts=2, initial_delay=0, jitter=0),
        transport=httpx.MockTransport(handler),
        sleep=lambda _: None,
    )

    with pytest.raises(OblidogConnectionError, match="HTTP 503"):
        transport.handle_request(request())

    assert attempts == 2


def test_exhaustion_raises_public_connection_error_with_cause() -> None:
    def handler(req: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("too slow", request=req)

    transport = ResilientTransport(
        policy=RetryPolicy(max_attempts=2, initial_delay=0, jitter=0),
        transport=httpx.MockTransport(handler),
        sleep=lambda _: None,
    )

    with pytest.raises(OblidogConnectionError) as exc_info:
        transport.handle_request(request())

    assert isinstance(exc_info.value.__cause__, httpx.ReadTimeout)


def test_mutating_request_is_never_replayed_after_transport_failure() -> None:
    attempts = 0

    def handler(req: httpx.Request) -> httpx.Response:
        nonlocal attempts
        attempts += 1
        raise httpx.ReadTimeout("ambiguous write", request=req)

    transport = ResilientTransport(
        policy=RetryPolicy(max_attempts=4, initial_delay=0, jitter=0),
        transport=httpx.MockTransport(handler),
        sleep=lambda _: None,
    )

    with pytest.raises(OblidogConnectionError):
        transport.handle_request(request("POST"))

    assert attempts == 1


def test_retry_policy_can_be_disabled() -> None:
    attempts = 0

    def handler(req: httpx.Request) -> httpx.Response:
        nonlocal attempts
        attempts += 1
        raise httpx.ConnectError("offline", request=req)

    transport = ResilientTransport(
        policy=RetryPolicy(enabled=False),
        transport=httpx.MockTransport(handler),
    )

    with pytest.raises(OblidogConnectionError):
        transport.handle_request(request())

    assert attempts == 1


def test_normal_client_error_is_not_retried() -> None:
    attempts = 0

    def handler(req: httpx.Request) -> httpx.Response:
        nonlocal attempts
        attempts += 1
        return httpx.Response(422, request=req)

    transport = ResilientTransport(
        policy=RetryPolicy(max_attempts=4, initial_delay=0, jitter=0),
        transport=httpx.MockTransport(handler),
    )

    assert transport.handle_request(request()).status_code == 422
    assert attempts == 1


def test_retry_delay_never_exceeds_max_delay() -> None:
    sleeps: list[float] = []

    def handler(req: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("offline", request=req)

    transport = ResilientTransport(
        policy=RetryPolicy(
            max_attempts=2,
            initial_delay=4,
            max_delay=4,
            jitter=1,
        ),
        transport=httpx.MockTransport(handler),
        sleep=sleeps.append,
        random_=lambda: 1.0,
    )

    with pytest.raises(OblidogConnectionError):
        transport.handle_request(request())

    assert sleeps == [4]


def test_policy_validates_configuration() -> None:
    with pytest.raises(ValueError, match="max_attempts"):
        RetryPolicy(max_attempts=0)
