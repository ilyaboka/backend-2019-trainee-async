from contextvars import ContextVar
from typing import Awaitable
from typing import Callable

from aiohttp import web

REQ_ID = ContextVar('X-Request-Id', default='None')
DEVICE_ID = ContextVar('X-Device-Id', default='None')


@web.middleware
async def set_context_vars(
    # pylint: disable=bad-continuation
    request: web.Request,
    handler: Callable[[web.Request], Awaitable[web.Response]],
) -> web.Response:
    # pylint: enable=bad-continuation
    """Проверят, является ли сессия завершённой"""
    REQ_ID.set(request.headers.get('Request-Id', 'None'))
    DEVICE_ID.set(request.headers.get('X-Device-Id', 'None'))
    responce: web.Response = await handler(request)
    return responce
