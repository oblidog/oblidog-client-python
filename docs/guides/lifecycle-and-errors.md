# Handle lifecycle decisions and failures

An integration must distinguish invalid obligation data from an unsuccessful
synchronization. `ERROR` is an alarm that the integration recognized invalid or
inconsistent data in Oblidog. A provider outage, login failure or network timeout
alone is a failed integration run; it is not a reason to mark an obligation
`ERROR`.

Ledger's [authoritative obligation lifecycle](https://github.com/oblidog/oblidog-ledger/blob/dev/docs/obligation-lifecycle.md)
defines allowed transitions and field effects. Consult it instead of assuming
all actions work from every state.

| SDK operation | Business intent |
| --- | --- |
| `mark_ready(period)` | Confirm complete, validated payment data and make the obligation ready for payment. |
| `mark_paid(period)` | Record a payment confirmed by the provider or another trusted source; importing an invoice alone is insufficient. |
| `cancel(period)` | Cancel an obligation that is being collected and should no longer be paid. |
| `reopen(period)` | Deliberately return a ready, paid, canceled or erroneous obligation to data collection so it can be corrected; clears `paid_at`. |
| `mark_error(period)` | Raise an alarm about invalid obligation data while preserving values, notes, components and payment timestamp. |

Updating values does not make an obligation ready automatically. Correct an
`ERROR` obligation by deliberately reopening it, correcting its data, and then
marking it ready. Do not automate reopening merely because an update was
rejected: that can undo a meaningful paid or canceled decision.

## Report recognized inconsistent data

Suppose your provider reconciliation has established that the total stored in
Oblidog is inconsistent. This reusable function appends a sanitized diagnostic,
raises the obligation alarm, and reports a failed run. Call it only after that
business validation has actually failed; it does not diagnose a mismatch itself.

```python
import os

from oblidog_client import OblidogClient, ObligationPeriod


def report_inconsistent_obligation(period: ObligationPeriod) -> None:
    with OblidogClient(
        base_url=os.environ["OBLIDOG_BASE_URL"],
        api_key=os.environ["OBLIDOG_API_KEY"],
    ) as client:
        with client.integrations.run() as run:
            client.obligations.append_note(
                period, "Reconciliation found an inconsistent invoice total"
            )
            client.obligations.mark_error(period)
            run.finish_failure(
                code="invalid_obligation_data",
                message="Invoice total needs review",
            )
```

Reporting run failure does not itself change the obligation lifecycle. Likewise,
marking an obligation `ERROR` does not finish the run. If the original
synchronization already has an active run, perform these calls inside that run
instead of starting a nested one.

## Catch SDK failures at the synchronization boundary

This complete entry point updates a known editable obligation. Configure the
environment and replace the sample invoice values as described in the
[import guide](obligation-import.md). Exceptions leave the run block before being
caught, allowing its context manager to report failure. Nonzero exit status lets
your scheduler detect failure.

```python
import datetime
import logging
import os

from oblidog_client import (
    OblidogApiError,
    OblidogClient,
    OblidogConflictError,
    OblidogConnectionError,
    OblidogError,
    OblidogValidationError,
    ObligationPeriod,
)

logger = logging.getLogger(__name__)


def main() -> int:
    try:
        with OblidogClient(
            base_url=os.environ["OBLIDOG_BASE_URL"],
            api_key=os.environ["OBLIDOG_API_KEY"],
        ) as client:
            with client.integrations.run() as run:
                client.obligations.update(
                    ObligationPeriod(2026, 8),
                    current_amount="425.30",
                    due_date=datetime.date(2026, 8, 20),
                )
                run.finish_success(changes_detected=None)
    except OblidogValidationError as error:
        logger.error("Request rejected (HTTP %s); review payload", error.status_code)
        return 1
    except OblidogConflictError as error:
        logger.error("Integration state conflict: %s", error.code.value)
        return 1
    except OblidogConnectionError:
        logger.error("API unavailable; reconcile writes before another attempt")
        return 1
    except OblidogApiError as error:
        logger.error("Unexpected API response (HTTP %s)", error.status_code)
        return 1
    except OblidogError:
        logger.error("Synchronization failed with an SDK error")
        return 1
    return 0


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    raise SystemExit(main())
```

Catch `OblidogConflictError` before `OblidogApiError` because it is a subclass.
Do not refresh the integration revision and blindly replay the invocation after
a conflict; check for another worker or a changed integration configuration.
A 422 rejects the request payload; it does not prove that stored obligation data
is inconsistent. Treat local `ValueError`/`TypeError` (such as an invalid
`ObligationPeriod`) as input or programming errors and correct them at the source.

`OblidogConnectionError` covers transport failures and exhausted retryable server
responses. Only reads are retried automatically. A timeout during a write can
mean the server applied it without returning a response. Read the current state
before deciding how to resume, especially after appending notes or creating
records without an external ID. The run wrapper attempts failure reporting on
an exception, but a disconnected API can prevent that report too.

API and validation exceptions retain `status_code` and raw response `content`.
Keep raw bodies, credentials, provider responses and exception tracebacks out of
user-facing notes and run failure messages. The handler logs only status codes
and typed conflict codes. See the [exceptions reference](../reference/exceptions.md),
[client/run reference](../reference/client.md), and
[obligations reference](../reference/obligations.md) for the supported contracts.
