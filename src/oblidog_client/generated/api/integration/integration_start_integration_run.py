from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.integration_conflict_response import IntegrationConflictResponse
from ...models.integration_public import IntegrationPublic
from ...models.integration_run_start import IntegrationRunStart
from ...types import Response


def _get_kwargs(
    integration_key: str,
    *,
    body: IntegrationRunStart,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/integration/instances/{integration_key}/start".format(
            integration_key=quote(str(integration_key), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | IntegrationConflictResponse | IntegrationPublic | None:
    if response.status_code == 200:
        response_200 = IntegrationPublic.from_dict(response.json())

        return response_200

    if response.status_code == 409:
        response_409 = IntegrationConflictResponse.from_dict(response.json())

        return response_409

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[HTTPValidationError | IntegrationConflictResponse | IntegrationPublic]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    integration_key: str,
    *,
    client: AuthenticatedClient,
    body: IntegrationRunStart,
) -> Response[HTTPValidationError | IntegrationConflictResponse | IntegrationPublic]:
    """Start Integration Run

    Args:
        integration_key (str):
        body (IntegrationRunStart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | IntegrationConflictResponse | IntegrationPublic]
    """

    kwargs = _get_kwargs(
        integration_key=integration_key,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    integration_key: str,
    *,
    client: AuthenticatedClient,
    body: IntegrationRunStart,
) -> HTTPValidationError | IntegrationConflictResponse | IntegrationPublic | None:
    """Start Integration Run

    Args:
        integration_key (str):
        body (IntegrationRunStart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | IntegrationConflictResponse | IntegrationPublic
    """

    return sync_detailed(
        integration_key=integration_key,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    integration_key: str,
    *,
    client: AuthenticatedClient,
    body: IntegrationRunStart,
) -> Response[HTTPValidationError | IntegrationConflictResponse | IntegrationPublic]:
    """Start Integration Run

    Args:
        integration_key (str):
        body (IntegrationRunStart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | IntegrationConflictResponse | IntegrationPublic]
    """

    kwargs = _get_kwargs(
        integration_key=integration_key,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    integration_key: str,
    *,
    client: AuthenticatedClient,
    body: IntegrationRunStart,
) -> HTTPValidationError | IntegrationConflictResponse | IntegrationPublic | None:
    """Start Integration Run

    Args:
        integration_key (str):
        body (IntegrationRunStart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | IntegrationConflictResponse | IntegrationPublic
    """

    return (
        await asyncio_detailed(
            integration_key=integration_key,
            client=client,
            body=body,
        )
    ).parsed
