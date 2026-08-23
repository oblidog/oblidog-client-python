from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.obligation_public import ObligationPublic
from ...types import Response


def _get_kwargs(
    obligation_key: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/integration/obligations/{obligation_key}/reopen".format(
            obligation_key=quote(str(obligation_key), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | ObligationPublic | None:
    if response.status_code == 200:
        response_200 = ObligationPublic.from_dict(response.json())

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
) -> Response[HTTPValidationError | ObligationPublic]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    obligation_key: str,
    *,
    client: AuthenticatedClient,
) -> Response[HTTPValidationError | ObligationPublic]:
    """Reopen Integration Obligation

    Args:
        obligation_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ObligationPublic]
    """

    kwargs = _get_kwargs(
        obligation_key=obligation_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    obligation_key: str,
    *,
    client: AuthenticatedClient,
) -> HTTPValidationError | ObligationPublic | None:
    """Reopen Integration Obligation

    Args:
        obligation_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ObligationPublic
    """

    return sync_detailed(
        obligation_key=obligation_key,
        client=client,
    ).parsed


async def asyncio_detailed(
    obligation_key: str,
    *,
    client: AuthenticatedClient,
) -> Response[HTTPValidationError | ObligationPublic]:
    """Reopen Integration Obligation

    Args:
        obligation_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ObligationPublic]
    """

    kwargs = _get_kwargs(
        obligation_key=obligation_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    obligation_key: str,
    *,
    client: AuthenticatedClient,
) -> HTTPValidationError | ObligationPublic | None:
    """Reopen Integration Obligation

    Args:
        obligation_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ObligationPublic
    """

    return (
        await asyncio_detailed(
            obligation_key=obligation_key,
            client=client,
        )
    ).parsed
