import datetime
from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.category_data_records_public import CategoryDataRecordsPublic
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    category_code: str,
    *,
    from_: datetime.datetime | None | Unset = UNSET,
    to: datetime.datetime | None | Unset = UNSET,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_from_: None | str | Unset
    if isinstance(from_, Unset):
        json_from_ = UNSET
    elif isinstance(from_, datetime.datetime):
        json_from_ = from_.isoformat()
    else:
        json_from_ = from_
    params["from"] = json_from_

    json_to: None | str | Unset
    if isinstance(to, Unset):
        json_to = UNSET
    elif isinstance(to, datetime.datetime):
        json_to = to.isoformat()
    else:
        json_to = to
    params["to"] = json_to

    params["limit"] = limit

    params["offset"] = offset

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/integration/categories/{category_code}/data-records".format(
            category_code=quote(str(category_code), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CategoryDataRecordsPublic | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = CategoryDataRecordsPublic.from_dict(response.json())

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
) -> Response[CategoryDataRecordsPublic | HTTPValidationError]:
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
    from_: datetime.datetime | None | Unset = UNSET,
    to: datetime.datetime | None | Unset = UNSET,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
) -> Response[CategoryDataRecordsPublic | HTTPValidationError]:
    """Read Integration Category Data Records

    Args:
        category_code (str):
        from_ (datetime.datetime | None | Unset):
        to (datetime.datetime | None | Unset):
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CategoryDataRecordsPublic | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        category_code=category_code,
        from_=from_,
        to=to,
        limit=limit,
        offset=offset,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    category_code: str,
    *,
    client: AuthenticatedClient,
    from_: datetime.datetime | None | Unset = UNSET,
    to: datetime.datetime | None | Unset = UNSET,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
) -> CategoryDataRecordsPublic | HTTPValidationError | None:
    """Read Integration Category Data Records

    Args:
        category_code (str):
        from_ (datetime.datetime | None | Unset):
        to (datetime.datetime | None | Unset):
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CategoryDataRecordsPublic | HTTPValidationError
    """

    return sync_detailed(
        category_code=category_code,
        client=client,
        from_=from_,
        to=to,
        limit=limit,
        offset=offset,
    ).parsed


async def asyncio_detailed(
    category_code: str,
    *,
    client: AuthenticatedClient,
    from_: datetime.datetime | None | Unset = UNSET,
    to: datetime.datetime | None | Unset = UNSET,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
) -> Response[CategoryDataRecordsPublic | HTTPValidationError]:
    """Read Integration Category Data Records

    Args:
        category_code (str):
        from_ (datetime.datetime | None | Unset):
        to (datetime.datetime | None | Unset):
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CategoryDataRecordsPublic | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        category_code=category_code,
        from_=from_,
        to=to,
        limit=limit,
        offset=offset,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    category_code: str,
    *,
    client: AuthenticatedClient,
    from_: datetime.datetime | None | Unset = UNSET,
    to: datetime.datetime | None | Unset = UNSET,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
) -> CategoryDataRecordsPublic | HTTPValidationError | None:
    """Read Integration Category Data Records

    Args:
        category_code (str):
        from_ (datetime.datetime | None | Unset):
        to (datetime.datetime | None | Unset):
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CategoryDataRecordsPublic | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            category_code=category_code,
            client=client,
            from_=from_,
            to=to,
            limit=limit,
            offset=offset,
        )
    ).parsed
