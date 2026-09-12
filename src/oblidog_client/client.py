from __future__ import annotations

import datetime
import logging
import uuid
from typing import Any, Self

from .exceptions import OblidogApiError, OblidogConflictError, OblidogValidationError
from .generated.api.integration import (
    integration_append_integration_obligation_note as append_note_api,
)
from .generated.api.integration import (
    integration_cancel_integration_obligation as cancel_api,
)
from .generated.api.integration import (
    integration_create_integration_category_data_record as create_category_data_api,
)
from .generated.api.integration import (
    integration_finish_integration_run as finish_run_api,
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
    integration_read_integration_category_data_records as list_category_data_api,
)
from .generated.api.integration import (
    integration_read_integration_category_data_schema as schema_category_data_api,
)
from .generated.api.integration import (
    integration_read_integration_context as read_context_api,
)
from .generated.api.integration import (
    integration_read_integration_obligation as get_api,
)
from .generated.api.integration import (
    integration_read_integration_obligation_components as list_components_api,
)
from .generated.api.integration import (
    integration_read_integration_obligations as list_api,
)
from .generated.api.integration import (
    integration_read_latest_integration_category_data_record as latest_category_data_api,
)
from .generated.api.integration import (
    integration_reopen_integration_obligation as reopen_api,
)
from .generated.api.integration import (
    integration_start_integration_run as start_run_api,
)
from .generated.api.integration import (
    integration_update_integration_obligation as update_api,
)
from .generated.api.integration import (
    integration_upsert_integration_obligation_component as upsert_component_api,
)
from .generated.client import AuthenticatedClient
from .generated.models.category_data_record_public import CategoryDataRecordPublic
from .generated.models.category_data_records_public import CategoryDataRecordsPublic
from .generated.models.category_data_schema_public import CategoryDataSchemaPublic
from .generated.models.http_validation_error import HTTPValidationError
from .generated.models.integration_category_data_record_create import (
    IntegrationCategoryDataRecordCreate,
)
from .generated.models.integration_category_data_record_create_data import (
    IntegrationCategoryDataRecordCreateData,
)
from .generated.models.integration_conflict_response import IntegrationConflictResponse
from .generated.models.integration_context_public import IntegrationContextPublic
from .generated.models.integration_obligation_component_upsert import (
    IntegrationObligationComponentUpsert,
)
from .generated.models.integration_obligation_component_upsert_metadata_type_0 import (
    IntegrationObligationComponentUpsertMetadataType0,
)
from .generated.models.integration_public import IntegrationPublic
from .generated.models.integration_result import IntegrationResult
from .generated.models.integration_run_error import IntegrationRunError
from .generated.models.integration_run_finish import IntegrationRunFinish
from .generated.models.integration_run_start import IntegrationRunStart
from .generated.models.obligation_component_public import ObligationComponentPublic
from .generated.models.obligation_components_public import ObligationComponentsPublic
from .generated.models.obligation_integration_update import ObligationIntegrationUpdate
from .generated.models.obligation_lifecycle import ObligationLifecycle
from .generated.models.obligation_note_append import ObligationNoteAppend
from .generated.models.obligation_public import ObligationPublic
from .generated.models.obligations_public import ObligationsPublic
from .generated.types import UNSET
from .period import ObligationPeriod

logger = logging.getLogger(__name__)


def _result(value: Any) -> Any:
    if isinstance(value, IntegrationConflictResponse):
        raise OblidogConflictError(value.detail.code)
    if isinstance(value, HTTPValidationError):
        raise OblidogValidationError(str(value.to_dict()))
    if value is None:
        raise OblidogApiError(0, b"API returned no parsed response")
    return value


def _period_path(period: ObligationPeriod) -> str:
    if not isinstance(period, ObligationPeriod):
        raise TypeError("period must be an ObligationPeriod")
    return str(period)


class ObligationsClient:
    """High-level synchronous operations for obligations owned by this integration.

    All methods use the category and integration associated with the API key.
    Documented validation responses raise :class:`OblidogValidationError`; API
    conflicts raise :class:`OblidogConflictError` where supported.
    """

    def __init__(self, client: AuthenticatedClient) -> None:
        self._client = client

    def list(
        self,
        *,
        year: int | None = None,
        month: int | None = None,
        lifecycle: ObligationLifecycle | None = None,
    ) -> ObligationsPublic:
        """List obligations visible to the authenticated integration.

        Args:
            year: Restrict results to a calendar year.
            month: Restrict results to a calendar month (1 through 12).
            lifecycle: Restrict results to one lifecycle state.

        Returns:
            A page-like collection of matching obligations.

        Raises:
            OblidogValidationError: If a supplied filter is invalid.
            OblidogApiError: If the API returns no parsed response.
        """
        result = list_api.sync(
            client=self._client,
            year=year if year is not None else UNSET,
            month=month if month is not None else UNSET,
            lifecycle=lifecycle if lifecycle is not None else UNSET,
        )
        return _result(result)

    def get(self, period: ObligationPeriod) -> ObligationPublic:
        """Return one obligation for ``period`` in the key-bound category.

        Raises:
            TypeError: If ``period`` is not an :class:`ObligationPeriod`.
            OblidogApiError: If the API cannot return a parsed obligation.
        """
        return _result(get_api.sync(_period_path(period), client=self._client))

    def list_components(self, period: ObligationPeriod) -> ObligationComponentsPublic:
        """List components currently attached to an obligation."""
        return _result(
            list_components_api.sync(_period_path(period), client=self._client)
        )

    def upsert_component(
        self,
        period: ObligationPeriod,
        *,
        type: str,
        label: str,
        external_id: str,
        amount: float | str | None | Any = UNSET,
        metadata: dict[str, Any] | None | Any = UNSET,
    ) -> ObligationComponentPublic:
        """Create or update a component identified by ``external_id``.

        ``amount`` and ``metadata`` distinguish omission from explicit
        ``None``: omitted values leave those fields out of the request, while
        ``None`` deliberately clears their value. ``external_id`` is required
        so repeated provider imports update the same component.

        Returns:
            The created or updated component.

        Raises:
            OblidogValidationError: If the request is invalid.
        """
        body = IntegrationObligationComponentUpsert(
            type_=type,
            label=label,
            external_id=external_id,
            amount=amount,
            metadata=(
                IntegrationObligationComponentUpsertMetadataType0.from_dict(metadata)
                if isinstance(metadata, dict)
                else metadata
            ),
        )
        return _result(
            upsert_component_api.sync(
                _period_path(period), client=self._client, body=body
            )
        )

    def update(
        self,
        period: ObligationPeriod,
        *,
        current_amount: float | str | None | Any = UNSET,
        due_date: datetime.date | None | Any = UNSET,
        issue_date: datetime.date | None | Any = UNSET,
    ) -> ObligationPublic:
        """Update integration-controlled values on an obligation.

        For every optional value, omission leaves it unchanged; explicit
        ``None`` clears it. This applies to ``current_amount``, ``due_date``,
        and ``issue_date``.

        Returns:
            The updated obligation.

        Raises:
            OblidogValidationError: If the update is invalid.
        """
        body = ObligationIntegrationUpdate(
            current_amount=current_amount,
            due_date=due_date,
            issue_date=issue_date,
        )
        return _result(
            update_api.sync(_period_path(period), client=self._client, body=body)
        )

    def append_note(self, period: ObligationPeriod, text: str) -> ObligationPublic:
        """Append ``text`` to an obligation's existing notes and return it."""
        return _result(
            append_note_api.sync(
                _period_path(period),
                client=self._client,
                body=ObligationNoteAppend(text=text),
            )
        )

    def mark_ready(self, period: ObligationPeriod) -> ObligationPublic:
        """Mark an obligation ready for payment."""
        return _result(mark_ready_api.sync(_period_path(period), client=self._client))

    def mark_paid(self, period: ObligationPeriod) -> ObligationPublic:
        """Mark an obligation paid."""
        return _result(mark_paid_api.sync(_period_path(period), client=self._client))

    def cancel(self, period: ObligationPeriod) -> ObligationPublic:
        """Cancel an obligation."""
        return _result(cancel_api.sync(_period_path(period), client=self._client))

    def reopen(self, period: ObligationPeriod) -> ObligationPublic:
        """Reopen a cancelled or completed obligation."""
        return _result(reopen_api.sync(_period_path(period), client=self._client))

    def mark_error(self, period: ObligationPeriod) -> ObligationPublic:
        """Mark an obligation as requiring attention after an integration error."""
        return _result(mark_error_api.sync(_period_path(period), client=self._client))


class CategoryDataClient:
    """Synchronous category data operations for the key-bound category."""

    def __init__(self, client: AuthenticatedClient) -> None:
        self._client = client

    def schema(self) -> CategoryDataSchemaPublic:
        """Return the active schema used to validate category observations."""
        return _result(schema_category_data_api.sync(client=self._client))

    def list(
        self,
        *,
        from_: datetime.datetime | None = None,
        to: datetime.datetime | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> CategoryDataRecordsPublic:
        """List category observations in an optional time range.

        ``from_`` and ``to`` are inclusive API filters when supplied. Omit
        either one to leave that end of the range unbounded.
        """
        return _result(
            list_category_data_api.sync(
                client=self._client,
                from_=from_ if from_ is not None else UNSET,
                to=to if to is not None else UNSET,
                limit=limit,
                offset=offset,
            )
        )

    def latest(self) -> CategoryDataRecordPublic:
        """Return the latest category observation."""
        return _result(latest_category_data_api.sync(client=self._client))

    def create(
        self,
        *,
        observed_at: datetime.datetime,
        data: dict[str, Any],
        external_id: str | None | Any = UNSET,
    ) -> CategoryDataRecordPublic:
        """Create a category observation.

        Args:
            observed_at: Time at which the source observed ``data``.
            data: Values conforming to :meth:`schema`.
            external_id: Provider-side identity used for idempotency. Omit it
                when the source has no stable identifier; pass ``None`` to
                explicitly send a null identifier.

        Returns:
            The created observation.

        Raises:
            OblidogValidationError: If the observation does not match schema.
        """
        body = IntegrationCategoryDataRecordCreate(
            observed_at=observed_at,
            data=IntegrationCategoryDataRecordCreateData.from_dict(data),
            external_id=external_id,
        )
        return _result(create_category_data_api.sync(client=self._client, body=body))


class IntegrationRun:
    """A started integration run that must be finished exactly once.

    Obtain instances with :meth:`IntegrationsClient.run` and normally use them
    as context managers. An exception before completion reports a sanitized
    failure and is then propagated to the caller.
    """

    def __init__(
        self,
        integrations: IntegrationsClient,
        *,
        context: IntegrationContextPublic,
        run_id: uuid.UUID,
    ) -> None:
        self.context = context
        self.run_id = run_id
        self._integrations = integrations
        self._finished = False

    def finish_success(self, *, changes_detected: bool | None) -> IntegrationPublic:
        """Report successful completion.

        Args:
            changes_detected: ``True`` when this run changed Ledger data,
                ``False`` for a known no-op, or ``None`` when unknown.

        Returns:
            The finished integration state.

        Raises:
            RuntimeError: If this run was already finished.
        """
        return self._finish(
            result=IntegrationResult.SUCCESS,
            changes_detected=changes_detected,
            error=None,
        )

    def finish_failure(
        self,
        *,
        code: str = "provider_failed",
        message: str = "Provider unavailable",
    ) -> IntegrationPublic:
        """Report a failure with a sanitized error summary.

        Never put credentials, raw provider responses, or tracebacks in
        ``message``.
        """
        return self._finish(
            result=IntegrationResult.FAILURE,
            changes_detected=None,
            error=IntegrationRunError(code=code, message=message),
        )

    def _finish(
        self,
        *,
        result: IntegrationResult,
        changes_detected: bool | None,
        error: IntegrationRunError | None,
    ) -> IntegrationPublic:
        if self._finished:
            raise RuntimeError("integration run has already been finished")
        finished = self._integrations.finish(
            run_id=self.run_id,
            result=result,
            changes_detected=changes_detected,
            error=error,
        )
        self._finished = True
        return finished

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type: object, *_: object) -> None:
        if self._finished:
            return
        if exc_type is None:
            self.finish_failure(
                code="run_incomplete",
                message="Integration run exited without completion",
            )
            return
        try:
            self.finish_failure(
                code="unhandled_exception",
                message="Integration run ended with an unhandled exception",
            )
        except Exception as error:
            # Preserve the original exception; callers may log the reporting
            # failure and retry it with the same run ID separately.
            logger.warning("Unable to report integration run failure", exc_info=error)


class IntegrationsClient:
    """Read authenticated integration context and report runs using its API key.

    Callers own run IDs and bounded retries. A conflict must never automatically
    refresh a revision and replay an old invocation.
    """

    def __init__(self, client: AuthenticatedClient) -> None:
        self._client = client

    def context(self) -> IntegrationContextPublic:
        """Return context associated with the authenticated integration API key.

        The returned object includes the integration and category selected by
        the API key. Its current revision is used by :meth:`run` for
        optimistic locking.
        """
        return _result(read_context_api.sync(client=self._client))

    def run(self) -> IntegrationRun:
        """Fetch context and start a run before synchronization work begins.

        The context's current revision is used for optimistic locking. Use the
        returned object as a context manager and finish it explicitly on the
        successful path.

        Example:
            ```python
            with client.integrations.run() as run:
                # synchronize using run.context
                run.finish_success(changes_detected=False)
            ```

        Raises:
            TypeError: If the context does not contain an integration object
                with an integer revision.
            OblidogConflictError: If another worker has changed state first.
        """
        context = self.context()
        expected_revision = context.integration.revision
        if not isinstance(expected_revision, int) or isinstance(
            expected_revision, bool
        ):
            raise TypeError(
                "integration context integration.revision must be an integer"
            )
        run_id = uuid.uuid4()
        self.start(run_id=run_id, expected_revision=expected_revision)
        return IntegrationRun(self, context=context, run_id=run_id)

    def start(
        self,
        *,
        run_id: uuid.UUID,
        expected_revision: int,
    ) -> IntegrationPublic:
        """Start a run using a caller-provided ID and expected revision.

        Prefer :meth:`run` for normal synchronization. This lower-level method
        is available when the caller explicitly owns scheduling and retries.

        Raises:
            OblidogConflictError: If the revision is stale or a run conflicts.
            OblidogValidationError: If the request is invalid.
        """
        return _result(
            start_run_api.sync(
                client=self._client,
                body=IntegrationRunStart(
                    run_id=run_id, expected_revision=expected_revision
                ),
            )
        )

    def finish(
        self,
        *,
        run_id: uuid.UUID,
        result: IntegrationResult,
        changes_detected: bool | None = None,
        error: IntegrationRunError | None = None,
    ) -> IntegrationPublic:
        """Finish a run using the same ID passed to :meth:`start`.

        ``changes_detected`` is required by the protocol as a value but can be
        ``None`` when its value is unknown. For failures, supply a sanitized
        ``error`` and avoid secrets or tracebacks.

        Raises:
            OblidogConflictError: If the run cannot be completed in its state.
            OblidogValidationError: If the completion request is invalid.
        """
        return _result(
            finish_run_api.sync(
                client=self._client,
                body=IntegrationRunFinish(
                    run_id=run_id,
                    result=result,
                    changes_detected=changes_detected,
                    error=error,
                ),
            )
        )


class OblidogClient:
    """Public synchronous client for the Oblidog integration API.

    Args:
        base_url: Root URL of the Oblidog Ledger API.
        api_key: Integration API key used as a bearer token.
        timeout: Per-request timeout in seconds.

    The client is a context manager; exiting it closes the underlying HTTP
    connection pool. Its ``obligations``, ``category_data``, and
    ``integrations`` attributes expose the supported SDK operations.
    """

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
        self.category_data = CategoryDataClient(self._client)
        self.integrations = IntegrationsClient(self._client)

    def close(self) -> None:
        """Close the underlying synchronous HTTP client."""
        self._client.get_httpx_client().close()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
