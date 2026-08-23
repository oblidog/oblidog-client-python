from __future__ import annotations

import datetime
from typing import Any

from .exceptions import FindogApiError, FindogValidationError
from .generated import errors
from .generated.api.integration import (
    integration_append_integration_obligation_note as append_note_api,
)
from .generated.api.integration import (
    integration_cancel_integration_obligation as cancel_api,
)
from .generated.api.integration import (
    integration_mark_integration_obligation_error as mark_error_api,
)
from .generated.api.integration import (
    integration_mark_integration_obligation_paid as mark_paid_api,
)
from .generated.api.integration import (
    integration_mark_integration_obligation_ready as mark_ready_api,
)
from .generated.api.integration import (
    integration_read_integration_obligation as get_api,
)
from .generated.api.integration import (
    integration_read_integration_obligations as list_api,
)
from .generated.api.integration import (
    integration_reopen_integration_obligation as reopen_api,
)
from .generated.api.integration import (
    integration_update_integration_obligation as update_api,
)
from .generated.client import AuthenticatedClient
from .generated.models.http_validation_error import HTTPValidationError
from .generated.models.obligation_integration_update import ObligationIntegrationUpdate
from .generated.models.obligation_lifecycle import ObligationLifecycle
from .generated.models.obligation_note_append import ObligationNoteAppend
from .generated.models.obligation_public import ObligationPublic
from .generated.models.obligations_public import ObligationsPublic
from .generated.types import UNSET


def _result(value: Any) -> Any:
    if isinstance(value, HTTPValidationError):
        raise FindogValidationError(str(value.to_dict()))
    if value is None:
        raise FindogApiError(0, b"API returned no parsed response")
    return value


class ObligationsClient:
    """High-level synchronous operations for integration obligations."""

    def __init__(self, client: AuthenticatedClient) -> None:
        self._client = client

    def list(
        self,
        *,
        year: int | None = None,
        month: int | None = None,
        category_code: str | None = None,
        lifecycle: ObligationLifecycle | None = None,
    ) -> ObligationsPublic:
        result = list_api.sync(
            client=self._client,
            year=year if year is not None else UNSET,
            month=month if month is not None else UNSET,
            category_code=category_code if category_code is not None else UNSET,
            lifecycle=lifecycle if lifecycle is not None else UNSET,
        )
        return _result(result)

    def get(self, obligation_key: str) -> ObligationPublic:
        return _result(get_api.sync(obligation_key, client=self._client))

    def update(
        self,
        obligation_key: str,
        *,
        current_amount: float | str | None | Any = UNSET,
        due_date: datetime.date | None | Any = UNSET,
        issue_date: datetime.date | None | Any = UNSET,
    ) -> ObligationPublic:
        body = ObligationIntegrationUpdate(
            current_amount=current_amount,
            due_date=due_date,
            issue_date=issue_date,
        )
        return _result(update_api.sync(obligation_key, client=self._client, body=body))

    def append_note(self, obligation_key: str, text: str) -> ObligationPublic:
        return _result(
            append_note_api.sync(
                obligation_key,
                client=self._client,
                body=ObligationNoteAppend(text=text),
            )
        )

    def mark_ready(self, obligation_key: str) -> ObligationPublic:
        return _result(mark_ready_api.sync(obligation_key, client=self._client))

    def mark_paid(self, obligation_key: str) -> ObligationPublic:
        return _result(mark_paid_api.sync(obligation_key, client=self._client))

    def cancel(self, obligation_key: str) -> ObligationPublic:
        return _result(cancel_api.sync(obligation_key, client=self._client))

    def reopen(self, obligation_key: str) -> ObligationPublic:
        return _result(reopen_api.sync(obligation_key, client=self._client))

    def mark_error(self, obligation_key: str) -> ObligationPublic:
        return _result(mark_error_api.sync(obligation_key, client=self._client))


class FindogClient:
    """Public synchronous client for the Findog integration API."""

    def __init__(
        self,
        *,
        base_url: str,
        api_key: str,
        timeout: float = 10.0,
    ) -> None:
        self._client = AuthenticatedClient(
            base_url=base_url.rstrip("/"),
            token=api_key,
            timeout=timeout,
            raise_on_unexpected_status=True,
        )
        self.obligations = ObligationsClient(self._client)

    def close(self) -> None:
        self._client.get_httpx_client().close()

    def __enter__(self) -> FindogClient:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
