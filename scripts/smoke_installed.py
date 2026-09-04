from __future__ import annotations

import importlib.util

from oblidog_client import (
    OblidogApiError,
    OblidogClient,
    OblidogError,
    OblidogValidationError,
)


def main() -> None:
    if importlib.util.find_spec("findog_client") is not None:
        raise SystemExit("Legacy findog_client package is importable")

    if not issubclass(OblidogApiError, OblidogError):
        raise SystemExit(
            "OblidogApiError is not part of the public exception hierarchy"
        )
    if not issubclass(OblidogValidationError, OblidogError):
        raise SystemExit(
            "OblidogValidationError is not part of the public exception hierarchy"
        )

    client = OblidogClient(
        base_url="https://oblidog.invalid",
        api_key="smoke-test-key",
    )
    if client.obligations is None or client.category_data is None:
        raise SystemExit("OblidogClient did not initialize its public resources")

    print("Installed oblidog_client public API smoke test passed")


if __name__ == "__main__":
    main()
