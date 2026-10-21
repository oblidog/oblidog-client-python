# Configure an integration

Give each integration its own API key in Ledger. The key selects one integration
and one category: SDK calls do not take a ledger ID or category code. Configure
the Oblidog server URL and key through your deployment's environment or secret
store; never commit a real key or print it in diagnostics.

Set `OBLIDOG_BASE_URL` to the server root, for example
`https://oblidog.example.com` (without `/api/v1`). Set `OBLIDOG_API_KEY` to the
integration key through your secret manager or local environment.

This complete connection check reads context without starting a synchronization:

```python
import os

from oblidog_client import OblidogClient

with OblidogClient(
    base_url=os.environ["OBLIDOG_BASE_URL"],
    api_key=os.environ["OBLIDOG_API_KEY"],
    timeout=15.0,
) as client:
    context = client.integrations.context()
    print(context.category.code)
```

`os.environ[...]` fails early if configuration is missing. The context manager
closes the HTTP client even when a request raises. Keep one client open for a
synchronization and wrap its work in `client.integrations.run()`; explicitly
call `run.finish_success(changes_detected=...)` after all steps succeed. An
exception escaping the run block reports a sanitized failure and propagates.
Leaving the block without finishing reports `run_incomplete`.

Use `datetime.date` for invoice dates and timezone-aware `datetime.datetime`
values for observations, for example `datetime.datetime.now(datetime.UTC)`.
Prefer the provider's actual observation timestamp when one is available; do not
silently interpret local wall time as UTC.

Continue with [importing an obligation](obligation-import.md),
[category observations](category-data.md), or
[lifecycle and failures](lifecycle-and-errors.md).
See [client and run reference](../reference/client.md) for configuration and
retry policy options.
