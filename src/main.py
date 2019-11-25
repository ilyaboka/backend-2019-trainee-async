import asyncio
import logging

from aiohttp import ClientSession
from aiohttp import web
from aiohttp_apispec import setup_aiohttp_apispec

import settings
from middleware import MIDDLEWARES
from routes import setup_routes


async def create_app() -> web.Application:
    """Инициализирует приложение"""
    application = web.Application(middlewares=MIDDLEWARES)
    application.cleanup_ctx.append(persistent_session)
    setup_routes(application)
    setup_aiohttp_apispec(application, **settings.APISPEC_CONF)
    return application


async def persistent_session(application) -> None:
    """Создаёт постоянную сессию"""
    application['persistent_session'] = session = ClientSession()
    yield
    await session.close()


logging.basicConfig(level=logging.INFO if settings.DEBUG else logging.WARNING)

LOOP = asyncio.get_event_loop()

if __name__ == '__main__':
    APP = create_app()
    web.run_app(APP, port=8118)
