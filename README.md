# oblidog-client

Python client for the Oblidog integration API.

Use the handwritten `OblidogClient` facade in application code. The
`oblidog_client.generated` namespace is OpenAPI-generated transport code and is
an implementation detail, not the recommended SDK API.

## Installation

```bash
pip install oblidog-client
```

## Usage

```python
import datetime

from oblidog_client import OblidogClient

with OblidogClient(base_url="https://oblidog.example.com", api_key="fdg_live_...") as client:
    with client.integrations.run() as run:
        client.category_data.create(
            observed_at=datetime.datetime.now(datetime.UTC),
            data={"meter_reading_kwh": 1234.5},
        )
        run.finish_success(changes_detected=True)
```

The integration API key selects its integration and category. Use
`client.integrations.run()` around synchronization work: it reads context and
starts a run before the block, then reports a sanitized failure if the block
raises.

## Documentation

The full documentation is published at
[oblidog.github.io/oblidog-client-python](https://oblidog.github.io/oblidog-client-python/).
It includes a quickstart, public API reference, and supported API boundary; it
intentionally excludes generated endpoints and transport classes.

## Development

This project uses `uv` for dependency and environment management. The low-level client is generated from the Oblidog Ledger integration OpenAPI contract; generated code should not be edited manually.

Run the same distribution verification used by CI locally:

```bash
./scripts/verify-package.sh
```

The command builds the wheel and source distribution, validates their metadata and contents, installs the wheel into a clean environment, and checks the installed public API. It does not publish any artifacts.

Release maintainers should follow the [Trusted Publishing setup and release procedure](docs/releasing.md).
