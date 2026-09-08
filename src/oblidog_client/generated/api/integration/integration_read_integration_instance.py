from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.integration_public import IntegrationPublic
from ...types import Response


def _get_kwargs(
    integration_key: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/integration/instances/{integration_key}".format(
            integration_key=quote(str(integration_key), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | IntegrationPublic | None:
    if response.status_code == 200:
        response_200 = IntegrationPublic.from_dict(response.json())

        return response_200

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[HTTPValidationError | IntegrationPublic]:
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
) -> Response[HTTPValidationError | IntegrationPublic]:
    """Read Integration Instance

    Args:
        integration_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | IntegrationPublic]
    """

    kwargs = _get_kwargs(
        integration_key=integration_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    integration_key: str,
    *,
    client: AuthenticatedClient,
) -> HTTPValidationError | IntegrationPublic | None:
    """Read Integration Instance

    Args:
        integration_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | IntegrationPublic
    """

    return sync_detailed(
        integration_key=integration_key,
        client=client,
    ).parsed


async def asyncio_detailed(
    integration_key: str,
    *,
    client: AuthenticatedClient,
) -> Response[HTTPValidationError | IntegrationPublic]:
    """Read Integration Instance

    Args:
        integration_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | IntegrationPublic]
    """

    kwargs = _get_kwargs(
        integration_key=integration_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    integration_key: str,
    *,
    client: AuthenticatedClient,
) -> HTTPValidationError | IntegrationPublic | None:
    """Read Integration Instance

    Args:
        integration_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | IntegrationPublic
    """

    return (
        await asyncio_detailed(
            integration_key=integration_key,
            client=client,
        )
    ).parsed
