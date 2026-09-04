# oblidog-client

Python client for the Oblidog integration API.

The generated OpenAPI client lives under `oblidog_client.generated` and is treated as an implementation detail. Integrations should normally use the handwritten `OblidogClient` facade.

## Installation

```bash
pip install oblidog-client
```

## Usage

```python
import datetime

from oblidog_client import OblidogClient, ObligationLifecycle

with OblidogClient(
    base_url="https://oblidog.example.com",
    api_key="fdg_live_...",
) as client:
    obligations = client.obligations.list(
        year=2026,
        month=8,
        lifecycle=ObligationLifecycle.READY,
    )

    obligation = client.obligations.update(
        "ENRG-2026-08",
        current_amount="425.30",
    )
    client.obligations.append_note(
        obligation.key,
        "Imported invoice FV/123/2026",
    )
    client.obligations.mark_ready(obligation.key)

    client.obligations.upsert_component(
        obligation.key,
        type="principal",
        label="August electricity",
        amount="425.30",
        metadata={"invoice_number": "FV/123/2026"},
    )
    components = client.obligations.list_components(obligation.key)

    record = client.category_data.create(
        "ENRG",
        observed_at=datetime.datetime(2026, 8, 1, tzinfo=datetime.UTC),
        data={"meter_reading_kwh": 1234.5},
        source="utility-import",
    )
    latest_record = client.category_data.latest("ENRG")
```

Category data operations are `schema`, `list`, `latest`, and `create`. Available obligation operations are `list`, `get`, `update`, `append_note`, `list_components`, `upsert_component`, `mark_ready`, `mark_paid`, `cancel`, `reopen`, and `mark_error`.

Unexpected HTTP statuses raise `OblidogApiError`/the generated transport exception rather than silently returning `None`. Validation responses are surfaced as `OblidogValidationError`.

## Development

This project uses `uv` for dependency and environment management. The low-level client is generated from the Oblidog Ledger integration OpenAPI contract; generated code should not be edited manually.

Run the same distribution verification used by CI locally:

```bash
./scripts/verify-package.sh
```

The command builds the wheel and source distribution, validates their metadata and contents, installs the wheel into a clean environment, and checks the installed public API. It does not publish any artifacts.
