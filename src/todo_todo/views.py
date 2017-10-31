from logging import getLogger

from aiohttp import web
from aiohttp.web_exceptions import HTTPMethodNotAllowed

from .models import Task


logger = getLogger(__name__)


class View(object):
    def __init__(self, request):
        self.request = request

    @classmethod
    async def dispatch(cls, request):
        view = cls(request)
        method = getattr(view, request.method.lower())

        if not method:
            return HTTPMethodNotAllowed()

        return await method()


class IndexView(View):
    async def get(self):
        return web.json_response(Task.all_objects())

    async def post(self):
        content = await self.request.json()
        return web.json_response(
            Task.create_object(content),
            status=201,
        )

    async def delete(self):
        Task.delete_all_objects()
        return web.json_response(Task.all_objects())


class TodoView(View):
    def __init__(self, request):
        super().__init__(request)
        self.uuid = request.match_info.get('uuid')

    async def get(self):
        return web.json_response(
            Task.get_object(self.uuid),
        )

    async def patch(self):
        content = await self.request.json()
        return web.json_response(
            Task.update_object(self.uuid, content),
        )

    async def delete(self):
        Task.delete_object(self.uuid)
        return Response()
