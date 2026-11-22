# Obligations

::: oblidog_client.ObligationsClient

::: oblidog_client.ObligationPeriod

::: oblidog_client.ObligationLifecycle

::: oblidog_client.PaymentExecution

`ObligationPublic.payment_execution` describes the user's plan for the individual
obligation:

| Value | Meaning |
| --- | --- |
| `None` | Manual payment |
| `PaymentExecution.SCHEDULED_TRANSFER` | A transfer already scheduled in the bank |
| `PaymentExecution.AUTOMATIC_COLLECTION` | An expected automatic collection, such as a subscription |

Import the enum from `oblidog_client`. An older server may omit the field, in
which case its value is unset and serialization leaves the field absent.
Integration value updates preserve the plan; the SDK does not expose an
integration operation to change it. A plan never confirms that payment occurred.
See [lifecycle decisions](../guides/lifecycle-and-errors.md#planned-payments)
for the effect on reminders and payment confirmation.

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
