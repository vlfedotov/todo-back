# -*- coding: utf-8 -*-

from json import dumps, loads
from logging import getLogger

from aiohttp import web
from aiohttp.web import Response
from aiohttp.web_exceptions import HTTPMethodNotAllowed

from .models import Task

logger = getLogger(__name__)


class JSONResponse(Response):
    def __init__(self, content, status=200):
        super().__init__(text=dumps(content), status=status)


class View(object):
    def __init__(self, request):
        self.request = request

    @classmethod
    async def dispatch(cls, request):
        view = cls(request)
        method = getattr(view, request.method.lower())
        logger.info("Serving %s %s", request.method, request.path)

        if not method:
            return HTTPMethodNotAllowed()

        return await method()

    async def options(self):
        return Response()


class IndexView(View):
    async def get(self):
        return web.json_response([])

    async def post(self):
        content = await self.request.json()
        print(content)
        return web.json_response(
            Task.create_object(content),
            status=201,
            dumps=dumps
        )

    async def delete(self):
        Task.delete_all_objects()
        return Response()


class TodoView(View):
    def __init__(self, request):
        super().__init__(request)
        self.uuid = request.match_info.get('uuid')

    async def get(self):
        return JSONResponse(Task.get_object(self.uuid))

    async def patch(self):
        content = await self.request.json()
        return JSONResponse(
            Task.update_object(self.uuid, content))

    async def delete(self):
        Task.delete_object(self.uuid)
        return Response()
