from __future__ import annotations

import logging
import random
import time
from collections.abc import Callable
from dataclasses import dataclass

import httpx

from .client import OblidogClient as BaseOblidogClient
from .exceptions import OblidogConnectionError

logger = logging.getLogger(__name__)

_RETRYABLE_METHODS = frozenset({"GET", "HEAD", "OPTIONS"})
_RETRYABLE_STATUS_CODES = frozenset({502, 503, 504})


@dataclass(frozen=True, slots=True)
class RetryPolicy:
    """Retry settings used by the high-level Oblidog client.

    Retries are deliberately limited to read-only HTTP methods. Mutating
    requests are attempted once because a transport failure can happen after
    the server has already applied the change.
    """

    enabled: bool = True
    max_attempts: int = 4
    initial_delay: float = 0.5
    max_delay: float = 4.0
    jitter: float = 0.25

    def __post_init__(self) -> None:
        if self.max_attempts < 1:
            raise ValueError("max_attempts must be at least 1")
        if self.initial_delay < 0:
            raise ValueError("initial_delay must not be negative")
        if self.max_delay < 0:
            raise ValueError("max_delay must not be negative")
        if self.jitter < 0:
            raise ValueError("jitter must not be negative")


class ResilientTransport(httpx.BaseTransport):
    """HTTP transport adding bounded retries and stable connection errors."""

    def __init__(
        self,
        *,
        policy: RetryPolicy,
        transport: httpx.BaseTransport | None = None,
        sleep: Callable[[float], None] = time.sleep,
        random_: Callable[[], float] = random.random,
    ) -> None:
        self._policy = policy
        self._transport = transport or httpx.HTTPTransport()
        self._sleep = sleep
        self._random = random_

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        retry_safe = request.method.upper() in _RETRYABLE_METHODS
        attempts = (
            self._policy.max_attempts if self._policy.enabled and retry_safe else 1
        )

        for attempt in range(1, attempts + 1):
            try:
                response = self._transport.handle_request(request)
            except httpx.TransportError as exc:
                if attempt >= attempts:
                    raise OblidogConnectionError(str(exc)) from exc
                self._wait(request, attempt, exc.__class__.__name__)
                continue

            if response.status_code not in _RETRYABLE_STATUS_CODES:
                return response
            if attempt >= attempts:
                status_code = response.status_code
                response.close()
                raise OblidogConnectionError(
                    f"Oblidog API remained unavailable after {attempts} attempt(s): "
                    f"HTTP {status_code}"
                )

            response.close()
            self._wait(request, attempt, f"HTTP {response.status_code}")

        raise AssertionError("retry loop exited unexpectedly")

    def _wait(self, request: httpx.Request, attempt: int, reason: str) -> None:
        exponential = self._policy.initial_delay * (2 ** (attempt - 1))
        delay = min(
            exponential + (self._policy.jitter * self._random()),
            self._policy.max_delay,
        )
        logger.warning(
            "Retrying Oblidog API request method=%s attempt=%d/%d delay=%.2fs reason=%s",
            request.method,
            attempt + 1,
            self._policy.max_attempts,
            delay,
            reason,
        )
        self._sleep(delay)

    def close(self) -> None:
        self._transport.close()


class OblidogClient(BaseOblidogClient):
    """High-level client with resilient, idempotency-aware HTTP transport."""

    def __init__(
        self,
        *,
        base_url: str,
        api_key: str,
        timeout: float = 10.0,
        retry_policy: RetryPolicy | None = None,
    ) -> None:
        super().__init__(base_url=base_url, api_key=api_key, timeout=timeout)
        policy = retry_policy or RetryPolicy()
        self._client._httpx_args["transport"] = ResilientTransport(policy=policy)
