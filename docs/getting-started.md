# Installation and quickstart

Install the package from PyPI:

```bash
pip install oblidog-client
```

Every synchronization should run inside `client.integrations.run()`. The
wrapper reads the integration context, starts a run using its current revision,
and reports a sanitized failure if the block raises.

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

The API key identifies the integration and its category. Do not use generated
endpoint functions directly in application code.
