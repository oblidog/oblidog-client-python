from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.integration_obligation_component_upsert import (
    IntegrationObligationComponentUpsert,
)
from ...models.obligation_component_public import ObligationComponentPublic
from ...types import Response


def _get_kwargs(
    period: str,
    *,
    body: IntegrationObligationComponentUpsert,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/v1/integration/obligations/{period}/components/upsert".format(
            period=quote(str(period), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | ObligationComponentPublic | None:
    if response.status_code == 200:
        response_200 = ObligationComponentPublic.from_dict(response.json())

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
) -> Response[HTTPValidationError | ObligationComponentPublic]:
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
    body: IntegrationObligationComponentUpsert,
) -> Response[HTTPValidationError | ObligationComponentPublic]:
    """Upsert Integration Obligation Component

    Args:
        period (str): Billing period in YYYY-MM format. Full obligation keys are temporarily
            accepted for client migration.
        body (IntegrationObligationComponentUpsert): An obligation component identified within its
            authenticated integration.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ObligationComponentPublic]
    """

    kwargs = _get_kwargs(
        period=period,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    period: str,
    *,
    client: AuthenticatedClient,
    body: IntegrationObligationComponentUpsert,
) -> HTTPValidationError | ObligationComponentPublic | None:
    """Upsert Integration Obligation Component

    Args:
        period (str): Billing period in YYYY-MM format. Full obligation keys are temporarily
            accepted for client migration.
        body (IntegrationObligationComponentUpsert): An obligation component identified within its
            authenticated integration.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ObligationComponentPublic
    """

    return sync_detailed(
        period=period,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    period: str,
    *,
    client: AuthenticatedClient,
    body: IntegrationObligationComponentUpsert,
) -> Response[HTTPValidationError | ObligationComponentPublic]:
    """Upsert Integration Obligation Component

    Args:
        period (str): Billing period in YYYY-MM format. Full obligation keys are temporarily
            accepted for client migration.
        body (IntegrationObligationComponentUpsert): An obligation component identified within its
            authenticated integration.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ObligationComponentPublic]
    """

    kwargs = _get_kwargs(
        period=period,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    period: str,
    *,
    client: AuthenticatedClient,
    body: IntegrationObligationComponentUpsert,
) -> HTTPValidationError | ObligationComponentPublic | None:
    """Upsert Integration Obligation Component

    Args:
        period (str): Billing period in YYYY-MM format. Full obligation keys are temporarily
            accepted for client migration.
        body (IntegrationObligationComponentUpsert): An obligation component identified within its
            authenticated integration.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ObligationComponentPublic
    """

    return (
        await asyncio_detailed(
            period=period,
            client=client,
            body=body,
        )
    ).parsed
