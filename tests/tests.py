# -*- coding: utf-8 -*-

import json

import requests

from asyncio import get_event_loop
from aiohttp.test_utils import TestClient, TestServer, loop_context

from ..todobackend import get_app, init


loop = get_event_loop()


app = get_app(loop)
# client = TestClient(TestServer(app), loop=loop)
loop.run_until_complete(init(loop))  #client.start_server())

#root = "http://127.0.0.1:8002"
async def test_empty_initial_list_of_tasks():
   resp = await requests.get("/")
   assert resp.status == 200
   assert await resp.text() == [] # 'we'
   # print(text)
   # text = json.loads(text)
   # assert await text == 0
# async def test_create_todo():
#    data = {
#        "user_id": 12,
#        "user": "vf",
#        "todo": "brush your teeth"
#    }
   
#    resp = await client.post("/", data=json.dumps(data))
#    assert resp.status == 201
#    print(await resp.json())
#    print(await resp.text())
#  # loop.run_until_complete(test_empty_initial_list_of_tasks())
# loop.run_until_complete(test_create_todo())
# loop.run_until_complete(client.close())
