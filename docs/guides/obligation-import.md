# Import an invoice into an obligation

Update an existing monthly obligation with a provider invoice, attach its line
items, then make it ready for payment. Ledger creates obligations according to
category recurrence; this recipe does not create a missing obligation.

First [configure the environment](configuration.md). The example assumes the
key-bound category has an August 2026 obligation in `DRAFT` or `COLLECTING_DATA`.
Replace the sample period, invoice dates, amount and identifiers with validated
provider data. The invoice currency must match the obligation currency.

```python
import datetime
import os

from oblidog_client import OblidogClient, ObligationLifecycle, ObligationPeriod

with OblidogClient(
    base_url=os.environ["OBLIDOG_BASE_URL"],
    api_key=os.environ["OBLIDOG_API_KEY"],
) as client:
    with client.integrations.run() as run:
        period = ObligationPeriod(2026, 8)
        obligation = client.obligations.get(period)
        print(obligation.key)

        # Alternative discovery: filter obligations in this category.
        candidates = client.obligations.list(
            year=2026,
            month=8,
            lifecycle=ObligationLifecycle.COLLECTING_DATA,
        )
        print([item.key for item in candidates.data])

        if obligation.lifecycle not in (
            ObligationLifecycle.DRAFT,
            ObligationLifecycle.COLLECTING_DATA,
        ):
            raise ValueError("Review the obligation lifecycle before importing")

        client.obligations.update(
            period,
            current_amount="425.30",
            issue_date=datetime.date(2026, 8, 1),
            due_date=datetime.date(2026, 8, 20),
        )
        result = client.obligations.upsert_component(
            period,
            type="principal",
            label="August electricity",
            external_id="invoice-FV-123-2026-line-1",
            amount="425.30",
            metadata={"invoice_number": "FV/123/2026"},
        )
        print(result.result)
        components = client.obligations.list_components(period)
        print([item.label for item in components.data])
        client.obligations.append_note(period, "Imported invoice FV/123/2026")
        client.obligations.mark_ready(period)
        run.finish_success(changes_detected=True)
```

The obligation key (such as `ENRG-2026-08`) is useful for display and diagnostics.
The supported lookup accepts `ObligationPeriod`, not the full key: use the year
and month from the provider, with the category supplied by the API key. A 404
means no visible obligation exists for that period; check the category and
recurrence instead of inventing a different key.

Supply money as decimal strings to avoid binary floating-point rounding.
Omitting an `update` argument preserves it; passing `None` explicitly clears it.
Components do not replace the obligation's amount: set the intended total with
`update`. Keep a stable component `external_id` across repeated imports so the
same line is updated rather than duplicated. The upsert's `result` is
`created`, `updated`, or `unchanged`.

This sequence is not a transaction. Earlier writes can remain if a later call
fails. Notes are appended on every call, and the entire sequence is not safe to
replay blindly. After a partial failure, read the obligation and components,
reconcile against the provider, and resume deliberately. In particular, avoid
reopening a paid or canceled obligation just to force an import through.

`mark_ready` belongs last, after successful validation and all intended writes.
For a known no-op report `changes_detected=False`; use `None` when you cannot
reliably determine whether data changed. See
[lifecycle and failures](lifecycle-and-errors.md) for recovery guidance and the
[obligations reference](../reference/obligations.md) for method signatures and
return models.
