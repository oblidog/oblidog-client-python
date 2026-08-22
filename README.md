# findog-client-python

Python client for the Findog integration API.

The project will contain:

- a generated low-level client based on the Findog integration OpenAPI contract,
- a small handwritten facade with an ergonomic public API,
- tests covering the supported client behavior.

## Development

This project uses `uv` for dependency and environment management.

Generation will be based on `openapi-python-client` and the OpenAPI snapshot stored under `openapi/`.
