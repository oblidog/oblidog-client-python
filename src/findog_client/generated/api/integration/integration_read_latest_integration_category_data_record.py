from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.category_data_record_public import CategoryDataRecordPublic
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    category_code: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/integration/categories/{category_code}/data-records/latest".format(
            category_code=quote(str(category_code), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CategoryDataRecordPublic | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = CategoryDataRecordPublic.from_dict(response.json())

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
) -> Response[CategoryDataRecordPublic | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    category_code: str,
    *,
    client: AuthenticatedClient,
) -> Response[CategoryDataRecordPublic | HTTPValidationError]:
    """Read Latest Integration Category Data Record

    Args:
        category_code (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CategoryDataRecordPublic | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        category_code=category_code,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    category_code: str,
    *,
    client: AuthenticatedClient,
) -> CategoryDataRecordPublic | HTTPValidationError | None:
    """Read Latest Integration Category Data Record

    Args:
        category_code (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CategoryDataRecordPublic | HTTPValidationError
    """

    return sync_detailed(
        category_code=category_code,
        client=client,
    ).parsed


async def asyncio_detailed(
    category_code: str,
    *,
    client: AuthenticatedClient,
) -> Response[CategoryDataRecordPublic | HTTPValidationError]:
    """Read Latest Integration Category Data Record

    Args:
        category_code (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CategoryDataRecordPublic | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        category_code=category_code,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    category_code: str,
    *,
    client: AuthenticatedClient,
) -> CategoryDataRecordPublic | HTTPValidationError | None:
    """Read Latest Integration Category Data Record

    Args:
        category_code (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CategoryDataRecordPublic | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            category_code=category_code,
            client=client,
        )
    ).parsed
