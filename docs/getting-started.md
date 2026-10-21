# Installation and quickstart

Install the package from PyPI:

```bash
pip install oblidog-client
```

[Configure the environment](guides/configuration.md) before running these
examples. The quickstart assumes an existing editable September 2026 obligation
and an active category schema accepting `meter_reading_kwh`.

Every synchronization should run inside `client.integrations.run()`. The
wrapper reads the integration context, starts a run using its current revision,
and reports a sanitized failure if the block raises.

```python
import datetime
import os

from oblidog_client import OblidogClient, ObligationPeriod

with OblidogClient(
    base_url=os.environ["OBLIDOG_BASE_URL"],
    api_key=os.environ["OBLIDOG_API_KEY"],
) as client:
    with client.integrations.run() as run:
        period = ObligationPeriod(2026, 9)
        client.obligations.update(
            period,
            current_amount="79.00",
            due_date=datetime.date(2026, 9, 20),
        )
        client.category_data.create(
            observed_at=datetime.datetime.now(datetime.UTC),
            data={"meter_reading_kwh": 1234.5},
        )
        client.obligations.mark_ready(period)
        run.finish_success(changes_detected=True)
```

The API key identifies the integration and its category. Do not use generated
endpoint functions directly in application code.

## Connection resilience

The high-level client retries transient connection failures and HTTP 502, 503,
and 504 responses for read-only requests (`GET`, `HEAD`, and `OPTIONS`). Retries
use bounded exponential backoff with jitter. Mutating requests are attempted
only once because a timeout can happen after the server has already applied the
change, and replaying such a request could duplicate a side effect.

When the API cannot be reached, or a retryable response remains unavailable
after all attempts, the client raises `OblidogConnectionError` instead of
leaking an `httpx` transport exception.

The default retry policy uses four attempts. It can be customized or disabled:

```python
import os

from oblidog_client import OblidogClient, RetryPolicy

retry_policy = RetryPolicy(
    max_attempts=3,
    initial_delay=0.25,
    max_delay=2.0,
    jitter=0.1,
)

with OblidogClient(
    base_url=os.environ["OBLIDOG_BASE_URL"],
    api_key=os.environ["OBLIDOG_API_KEY"],
    retry_policy=retry_policy,
) as client:
    context = client.integrations.context()
```

To disable automatic retries while retaining the stable connection exception,
pass `RetryPolicy(enabled=False)`.

Continue with the [complete invoice import](guides/obligation-import.md) or
[category observations](guides/category-data.md) recipes.
