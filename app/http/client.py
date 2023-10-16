import json
from typing import Optional

import backoff
import httpx
import ujson

from app.http import exceptions


DEFAULT_HEADERS = {"Content-Type": "application/json"}
DEFAULT_TIMEOUTS = (3, 10)


def error_handler(func):
    async def decorator(*args, **kwargs):
        try:
            response = await func(*args, **kwargs)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            try:
                error = e.response.json()
            except json.decoder.JSONDecodeError:
                error = None
            status_code = e.response.status_code
            if status_code == 401:
                raise exceptions.ServiceUnauthorized(
                    e,
                    url=e.request.url,
                    status_code=status_code,
                    error=error,
                    body=str(e.request.content),
                    headers=e.request.headers,
                )
            elif status_code == 403:
                raise exceptions.ServiceForbidden(
                    e,
                    url=e.request.url,
                    status_code=status_code,
                    error=error,
                    body=str(e.request.content),
                    headers=e.request.headers,
                )
            elif status_code == 404 or 400:
                raise exceptions.NotFound(
                    e,
                    url=e.request.url,
                    status_code=status_code,
                    error=error,
                    body=str(e.request.content),
                    headers=e.request.headers,
                )
            raise exceptions.ServiceError(
                e, url=e.request.url, status_code=status_code, error=error
            )
        except httpx.RequestError as e:
            raise exceptions.ServiceException(e, url=e.request.url)
        return response

    return decorator


async def get_headers(headers: Optional[dict]) -> dict:
    if not headers:
        return DEFAULT_HEADERS
    return {**DEFAULT_HEADERS, **headers}


class HttpClient:
    def __init__(self):
        self.client: httpx.AsyncClient | None = None

    def init(self):
        self.client = httpx.AsyncClient()

    @backoff.on_exception(
        backoff.expo,
        exceptions.ServiceUnavailable,
        max_tries=2,
        logger=None,
    )
    @error_handler
    async def post(
        self,
        url: str,
        body: Optional[dict] = None,
        headers: Optional[dict] = None,
        timeout=DEFAULT_TIMEOUTS,
    ):
        if not body:
            body = {}
        headers = await get_headers(headers=headers)
        return await self.client.post(
            url=url, data=ujson.dumps(body), headers=headers, timeout=timeout
        )

    @backoff.on_exception(
        backoff.expo,
        exceptions.ServiceUnavailable,
        max_tries=2,
        logger=None,
    )
    @error_handler
    async def put(
        self,
        url: str,
        body: dict,
        headers: Optional[dict] = None,
        timeout=DEFAULT_TIMEOUTS,
    ):
        headers = await get_headers(headers=headers)
        return await self.client.put(
            url=url, data=ujson.dumps(body), headers=headers, timeout=timeout
        )

    @backoff.on_exception(
        backoff.expo,
        exceptions.ServiceUnavailable,
        max_tries=2,
        logger=None,
    )
    @error_handler
    async def get(self, url: str, headers: Optional[dict] = None, timeout=DEFAULT_TIMEOUTS):
        return await self.client.get(url=url, headers=headers, timeout=timeout)

    @backoff.on_exception(
        backoff.expo,
        exceptions.ServiceUnavailable,
        max_tries=2,
        logger=None,
    )
    @error_handler
    async def head(self, url: str, headers: Optional[dict] = None, timeout=DEFAULT_TIMEOUTS):
        return await self.client.head(url=url, headers=headers, timeout=timeout)

    @error_handler
    async def patch(
        self,
        url: str,
        body: dict,
        headers: Optional[dict] = None,
        timeout=DEFAULT_TIMEOUTS,
    ):
        headers = await get_headers(headers=headers)
        return await self.client.patch(
            url=url, data=ujson.dumps(body), headers=headers, timeout=timeout
        )


client = HttpClient()
