from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error_response import ApiErrorResponse
from ...models.integration_conflict_response import IntegrationConflictResponse
from ...models.integration_public import IntegrationPublic
from ...models.integration_run_finish import IntegrationRunFinish
from ...types import Response


def _get_kwargs(
    *,
    body: IntegrationRunFinish,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/integration/runs/finish",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ApiErrorResponse | IntegrationConflictResponse | IntegrationPublic | None:
    if response.status_code == 200:
        response_200 = IntegrationPublic.from_dict(response.json())

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
        response_409 = IntegrationConflictResponse.from_dict(response.json())

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
) -> Response[ApiErrorResponse | IntegrationConflictResponse | IntegrationPublic]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: IntegrationRunFinish,
) -> Response[ApiErrorResponse | IntegrationConflictResponse | IntegrationPublic]:
    """Finish Integration Run

    Args:
        body (IntegrationRunFinish):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiErrorResponse | IntegrationConflictResponse | IntegrationPublic]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: IntegrationRunFinish,
) -> ApiErrorResponse | IntegrationConflictResponse | IntegrationPublic | None:
    """Finish Integration Run

    Args:
        body (IntegrationRunFinish):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiErrorResponse | IntegrationConflictResponse | IntegrationPublic
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: IntegrationRunFinish,
) -> Response[ApiErrorResponse | IntegrationConflictResponse | IntegrationPublic]:
    """Finish Integration Run

    Args:
        body (IntegrationRunFinish):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiErrorResponse | IntegrationConflictResponse | IntegrationPublic]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: IntegrationRunFinish,
) -> ApiErrorResponse | IntegrationConflictResponse | IntegrationPublic | None:
    """Finish Integration Run

    Args:
        body (IntegrationRunFinish):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiErrorResponse | IntegrationConflictResponse | IntegrationPublic
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
