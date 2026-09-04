from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.obligation_lifecycle import ObligationLifecycle
from ...models.obligations_public import ObligationsPublic
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    year: int | None | Unset = UNSET,
    month: int | None | Unset = UNSET,
    category_code: None | str | Unset = UNSET,
    lifecycle: None | ObligationLifecycle | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_year: int | None | Unset
    if isinstance(year, Unset):
        json_year = UNSET
    else:
        json_year = year
    params["year"] = json_year

    json_month: int | None | Unset
    if isinstance(month, Unset):
        json_month = UNSET
    else:
        json_month = month
    params["month"] = json_month

    json_category_code: None | str | Unset
    if isinstance(category_code, Unset):
        json_category_code = UNSET
    else:
        json_category_code = category_code
    params["category_code"] = json_category_code

    json_lifecycle: None | str | Unset
    if isinstance(lifecycle, Unset):
        json_lifecycle = UNSET
    elif isinstance(lifecycle, ObligationLifecycle):
        json_lifecycle = lifecycle.value
    else:
        json_lifecycle = lifecycle
    params["lifecycle"] = json_lifecycle

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/integration/obligations",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | ObligationsPublic | None:
    if response.status_code == 200:
        response_200 = ObligationsPublic.from_dict(response.json())

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
) -> Response[HTTPValidationError | ObligationsPublic]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    year: int | None | Unset = UNSET,
    month: int | None | Unset = UNSET,
    category_code: None | str | Unset = UNSET,
    lifecycle: None | ObligationLifecycle | Unset = UNSET,
) -> Response[HTTPValidationError | ObligationsPublic]:
    """Read Integration Obligations

    Args:
        year (int | None | Unset):
        month (int | None | Unset):
        category_code (None | str | Unset):
        lifecycle (None | ObligationLifecycle | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ObligationsPublic]
    """

    kwargs = _get_kwargs(
        year=year,
        month=month,
        category_code=category_code,
        lifecycle=lifecycle,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    year: int | None | Unset = UNSET,
    month: int | None | Unset = UNSET,
    category_code: None | str | Unset = UNSET,
    lifecycle: None | ObligationLifecycle | Unset = UNSET,
) -> HTTPValidationError | ObligationsPublic | None:
    """Read Integration Obligations

    Args:
        year (int | None | Unset):
        month (int | None | Unset):
        category_code (None | str | Unset):
        lifecycle (None | ObligationLifecycle | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ObligationsPublic
    """

    return sync_detailed(
        client=client,
        year=year,
        month=month,
        category_code=category_code,
        lifecycle=lifecycle,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    year: int | None | Unset = UNSET,
    month: int | None | Unset = UNSET,
    category_code: None | str | Unset = UNSET,
    lifecycle: None | ObligationLifecycle | Unset = UNSET,
) -> Response[HTTPValidationError | ObligationsPublic]:
    """Read Integration Obligations

    Args:
        year (int | None | Unset):
        month (int | None | Unset):
        category_code (None | str | Unset):
        lifecycle (None | ObligationLifecycle | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ObligationsPublic]
    """

    kwargs = _get_kwargs(
        year=year,
        month=month,
        category_code=category_code,
        lifecycle=lifecycle,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    year: int | None | Unset = UNSET,
    month: int | None | Unset = UNSET,
    category_code: None | str | Unset = UNSET,
    lifecycle: None | ObligationLifecycle | Unset = UNSET,
) -> HTTPValidationError | ObligationsPublic | None:
    """Read Integration Obligations

    Args:
        year (int | None | Unset):
        month (int | None | Unset):
        category_code (None | str | Unset):
        lifecycle (None | ObligationLifecycle | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ObligationsPublic
    """

    return (
        await asyncio_detailed(
            client=client,
            year=year,
            month=month,
            category_code=category_code,
            lifecycle=lifecycle,
        )
    ).parsed
