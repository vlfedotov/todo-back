# -*- coding: utf-8 -*-

import json

import pytest

from todo_todo.todo_todo.models import Task
from ..todo_todo import get_app


@pytest.fixture
def client(loop, test_client):
    return loop.run_until_complete(test_client(get_app))


@pytest.fixture
def todo(client):
    data = {
        'user_id': 12,
        'user': 'vf',
        'todo': 'wash the car'
    }

    return client.post('/', data=json.dumps(data))


async def test_hello(client):
    resp = await client.get('/')
    assert resp.status == 200

    assert [] == await resp.json()


async def test_create_todo(client):
    data = {
        'user_id': 12,
        'user': 'vf',
        'todo': 'brush your teeth'
    }

    resp = await client.post('/', data=json.dumps(data))
    assert resp.status == 201

    res = await resp.json()
    assert res['user'] == data['user']
    assert res['user_id'] == data['user_id']
    assert res['todo'] == data['todo']
    assert res['completed'] is False


async def test_get_todo_fixture(client, todo):
    task = Task.all_objects()[0]
    resp = await client.get('/{}'.format(task['uuid']))
    assert resp.status == 200

    res = await resp.json()
    assert res['uuid'] == task['uuid']


async def test_complete_todo(client, todo):
    assert len(Task.all_objects()) == 1

    t = Task.all_objects()[0]
    assert t['completed'] is False

    update = {
        'completed': True
    }

    resp = await client.patch('/{}'.format(t['uuid']), data=json.dumps(update))
    assert resp.status == 200

    res = await resp.json()
    assert res['completed'] is True


async def testdelete_todo(client, todo):
    pass
