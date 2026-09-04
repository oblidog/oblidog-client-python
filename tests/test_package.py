from __future__ import annotations

import importlib.util

import oblidog_client

EXPECTED_PUBLIC_API = {
    "CategoryDataClient",
    "CategoryDataRecordPublic",
    "CategoryDataRecordsPublic",
    "CategoryDataSchemaPublic",
    "ObligationComponentPublic",
    "ObligationComponentsPublic",
    "ObligationLifecycle",
    "ObligationPublic",
    "ObligationsClient",
    "ObligationsPublic",
    "OblidogApiError",
    "OblidogClient",
    "OblidogError",
    "OblidogValidationError",
}


def test_package_imports() -> None:
    assert oblidog_client.__doc__
    assert set(oblidog_client.__all__) == EXPECTED_PUBLIC_API


def test_legacy_namespace_is_not_importable() -> None:
    assert importlib.util.find_spec("findog_client") is None
