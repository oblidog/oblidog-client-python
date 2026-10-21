# Store and read category observations

Keep timestamped provider measurements, such as meter readings, separately from
invoice amounts. A category must already have an active data schema configured
in Ledger. This example expects a schema accepting a numeric
`meter_reading_kwh` property; adapt the payload to your category's schema.

After [configuring the environment](configuration.md), this complete example
inspects the schema, stores one observation, reads the latest observation, and
walks all records in a bounded time range:

```python
import datetime
import os

from oblidog_client import OblidogClient

with OblidogClient(
    base_url=os.environ["OBLIDOG_BASE_URL"],
    api_key=os.environ["OBLIDOG_API_KEY"],
) as client:
    with client.integrations.run() as run:
        schema = client.category_data.schema()
        print(schema.version, schema.schema.to_dict())

        # Sample provider timestamp and stable reading identity.
        observed_at = datetime.datetime(2026, 8, 1, 10, tzinfo=datetime.UTC)
        record = client.category_data.create(
            observed_at=observed_at,
            data={"meter_reading_kwh": 1234.5},
            external_id="meter-42-reading-2026-08-01T10:00:00Z",
        )
        print(record.id, record.source, record.schema_version)
        latest = client.category_data.latest()
        print(latest.observed_at, latest.data.to_dict())

        offset = 0
        while True:
            page = client.category_data.list(
                from_=datetime.datetime(2026, 8, 1, tzinfo=datetime.UTC),
                to=datetime.datetime(2026, 8, 31, 23, 59, 59, tzinfo=datetime.UTC),
                limit=100,
                offset=offset,
            )
            if not page.data:
                break
            for observation in page.data:
                print(observation.observed_at, observation.data.to_dict())
            offset += len(page.data)

        run.finish_success(changes_detected=None)
```

`from_` and `to` are inclusive observation-time filters; the trailing underscore
avoids Python's reserved `from` keyword. Keep the same bounds while paginating
and advance `offset` by the number of returned records. Offset pagination is not
a snapshot: concurrent inserts can shift pages. The example reports unknown
changes because a repeated external identity may already exist.

`source` is assigned by Ledger from the authenticated integration's name; it is
returned on records and is not an argument to `create`. `external_id` is an
optional stable provider identity used for idempotency. Reuse it for the same
observation, not for different readings. Omit it when no stable identity exists
(or pass `None` explicitly); do not assume unidentified repeated submissions
will be deduplicated. Do not generate a fresh random ID for each retry.

The active schema validates submitted `data`. A schema rejection raises
`OblidogValidationError`. No active schema or no latest observation can produce
an API error; handle these as setup or empty-history conditions as appropriate
for the returned status. `latest()` refers to the category's latest observation,
which need not be the record just submitted if newer data already exists.

See [category-data reference](../reference/category-data.md) for models and
arguments, and [failure handling](lifecycle-and-errors.md) for a copyable handler.
