# Obligations

::: oblidog_client.ObligationsClient

::: oblidog_client.ObligationPeriod

::: oblidog_client.ObligationLifecycle

::: oblidog_client.ObligationPublic

::: oblidog_client.ObligationsPublic

::: oblidog_client.ObligationComponentPublic

::: oblidog_client.ObligationComponentUpsertResult

::: oblidog_client.MutationResult

`MutationResult` indicates what the component upsert actually changed:

| Value | Meaning |
| --- | --- |
| `created` | A new component was created. |
| `updated` | An existing component was changed. |
| `unchanged` | The submitted component matched the stored component, so no change was persisted. |

::: oblidog_client.ObligationComponentsPublic
