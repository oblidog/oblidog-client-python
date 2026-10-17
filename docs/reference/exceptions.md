# Exceptions

The high-level client raises SDK exceptions for HTTP error responses rather
than returning error models as operation results:

- HTTP 422 raises `OblidogValidationError`.
- Typed integration run conflicts raise `OblidogConflictError`; its `code`
  contains the integration conflict reason.
- Other HTTP errors raise `OblidogApiError`.

These exceptions preserve the original HTTP status in `status_code` and the
complete response bytes in `content`, including error codes and `params`.
Undocumented statuses also raise `OblidogApiError` with the generated exception
retained as the cause.

::: oblidog_client.OblidogError

::: oblidog_client.OblidogApiError

::: oblidog_client.OblidogValidationError

::: oblidog_client.OblidogConflictError

::: oblidog_client.OblidogConnectionError
