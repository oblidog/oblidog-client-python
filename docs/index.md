# Oblidog Python Client

`oblidog-client` is the supported synchronous Python SDK for an Oblidog
integration. Use the handwritten `OblidogClient` facade for all application
code.

The `oblidog_client.generated` namespace contains OpenAPI-generated transport
code. It is an implementation detail: it is not part of the recommended SDK
surface and is intentionally absent from this reference.

Start with [installation and quickstart](getting-started.md), then use the API
reference for the exported public symbols.

For complete business workflows, follow the integration guides:

- [Configure an integration](guides/configuration.md).
- [Import an invoice into an obligation](guides/obligation-import.md).
- [Store and read category observations](guides/category-data.md).
- [Handle lifecycle decisions and failures](guides/lifecycle-and-errors.md).
