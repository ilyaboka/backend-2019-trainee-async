import asyncio
import logging

from aiohttp import web
from aiohttp_apispec import setup_aiohttp_apispec

import settings
from middleware import MIDDLEWARES
from routes import setup_routes


async def create_app() -> web.Application:
    """Инициализирует приложение"""
    application = web.Application(middlewares=MIDDLEWARES)
    setup_routes(application)
    setup_aiohttp_apispec(application, **settings.APISPEC_CONF)
    return application


logging.basicConfig(level=logging.INFO if settings.DEBUG else logging.WARNING)

LOOP = asyncio.get_event_loop()

if __name__ == '__main__':
    APP = create_app()
    web.run_app(APP, port=8118)
