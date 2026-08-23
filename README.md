# findog-client-python

Python client for the Findog integration API.

The generated OpenAPI client lives under `findog_client.generated` and is treated as an implementation detail. Integrations should normally use the handwritten `FindogClient` facade.

## Usage

```python
from findog_client import FindogClient, ObligationLifecycle

with FindogClient(
    base_url="https://findog.example.com",
    api_key="fdg_live_...",
) as client:
    obligations = client.obligations.list(
        year=2026,
        month=8,
        lifecycle=ObligationLifecycle.READY,
    )

    obligation = client.obligations.update(
        "enea-2026-08",
        current_amount="425.30",
    )
    client.obligations.append_note(
        obligation.key,
        "Imported invoice FV/123/2026",
    )
    client.obligations.mark_ready(obligation.key)
```

Available obligation operations are `list`, `get`, `update`, `append_note`, `mark_ready`, `mark_paid`, `cancel`, `reopen`, and `mark_error`.

Unexpected HTTP statuses raise `FindogApiError`/the generated transport exception rather than silently returning `None`. Validation responses are surfaced as `FindogValidationError`.

## Development

This project uses `uv` for dependency and environment management. The low-level client is generated from the Findog Ledger integration OpenAPI contract; generated code should not be edited manually.
