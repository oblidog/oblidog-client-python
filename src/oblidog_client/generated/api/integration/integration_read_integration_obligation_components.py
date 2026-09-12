from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.obligation_components_public import ObligationComponentsPublic
from ...types import Response


def _get_kwargs(
    period: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/integration/obligations/{period}/components".format(
            period=quote(str(period), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | ObligationComponentsPublic | None:
    if response.status_code == 200:
        response_200 = ObligationComponentsPublic.from_dict(response.json())

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
) -> Response[HTTPValidationError | ObligationComponentsPublic]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    period: str,
    *,
    client: AuthenticatedClient,
) -> Response[HTTPValidationError | ObligationComponentsPublic]:
    """Read Integration Obligation Components

    Args:
        period (str): Billing period in YYYY-MM format. Full obligation keys are temporarily
            accepted for client migration.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ObligationComponentsPublic]
    """

    kwargs = _get_kwargs(
        period=period,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    period: str,
    *,
    client: AuthenticatedClient,
) -> HTTPValidationError | ObligationComponentsPublic | None:
    """Read Integration Obligation Components

    Args:
        period (str): Billing period in YYYY-MM format. Full obligation keys are temporarily
            accepted for client migration.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ObligationComponentsPublic
    """

    return sync_detailed(
        period=period,
        client=client,
    ).parsed


async def asyncio_detailed(
    period: str,
    *,
    client: AuthenticatedClient,
) -> Response[HTTPValidationError | ObligationComponentsPublic]:
    """Read Integration Obligation Components

    Args:
        period (str): Billing period in YYYY-MM format. Full obligation keys are temporarily
            accepted for client migration.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ObligationComponentsPublic]
    """

    kwargs = _get_kwargs(
        period=period,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    period: str,
    *,
    client: AuthenticatedClient,
) -> HTTPValidationError | ObligationComponentsPublic | None:
    """Read Integration Obligation Components

    Args:
        period (str): Billing period in YYYY-MM format. Full obligation keys are temporarily
            accepted for client migration.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ObligationComponentsPublic
    """

    return (
        await asyncio_detailed(
            period=period,
            client=client,
        )
    ).parsed
