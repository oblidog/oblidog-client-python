from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error_response import ApiErrorResponse
from ...models.integration_obligation_component_upsert import (
    IntegrationObligationComponentUpsert,
)
from ...models.obligation_component_upsert_result import ObligationComponentUpsertResult
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
) -> ApiErrorResponse | ObligationComponentUpsertResult | None:
    if response.status_code == 200:
        response_200 = ObligationComponentUpsertResult.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ApiErrorResponse.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ApiErrorResponse.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ApiErrorResponse.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = ApiErrorResponse.from_dict(response.json())

        return response_404

    if response.status_code == 409:
        response_409 = ApiErrorResponse.from_dict(response.json())

        return response_409

    if response.status_code == 413:
        response_413 = ApiErrorResponse.from_dict(response.json())

        return response_413

    if response.status_code == 422:
        response_422 = ApiErrorResponse.from_dict(response.json())

        return response_422

    if response.status_code == 500:
        response_500 = ApiErrorResponse.from_dict(response.json())

        return response_500

    if response.status_code == 503:
        response_503 = ApiErrorResponse.from_dict(response.json())

        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ApiErrorResponse | ObligationComponentUpsertResult]:
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
) -> Response[ApiErrorResponse | ObligationComponentUpsertResult]:
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
        Response[ApiErrorResponse | ObligationComponentUpsertResult]
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
) -> ApiErrorResponse | ObligationComponentUpsertResult | None:
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
        ApiErrorResponse | ObligationComponentUpsertResult
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
) -> Response[ApiErrorResponse | ObligationComponentUpsertResult]:
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
        Response[ApiErrorResponse | ObligationComponentUpsertResult]
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
) -> ApiErrorResponse | ObligationComponentUpsertResult | None:
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
        ApiErrorResponse | ObligationComponentUpsertResult
    """

    return (
        await asyncio_detailed(
            period=period,
            client=client,
            body=body,
        )
    ).parsed
