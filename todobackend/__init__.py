from logging import getLogger, basicConfig, INFO
from os import getenv
from aiohttp import web

from .middleware import cors_middleware_factory
from .views import (
    IndexView,
    TodoView,
)


basicConfig(level=INFO)
logger = getLogger(__name__)


IP = getenv('IP', '0.0.0.0')
PORT = getenv('PORT', '8000')


def get_app(loop):
    app = web.Application(loop=loop, middlewares=[cors_middleware_factory])

    # Routes
    app.router.add_route('*', '/', IndexView.dispatch)
    app.router.add_route('*', '/{uuid}', TodoView.dispatch)

    return app


async def init(loop):
    app = get_app(loop)
    
    # Config
    logger.info("Starting server at %s:%s", IP, PORT)
    srv = await loop.create_server(app.make_handler(), IP, PORT)
    return srv
