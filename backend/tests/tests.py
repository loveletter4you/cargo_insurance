import json
import os
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from tortoise import Tortoise

from main import app, app_factory, app_startup
from settings_env import ADMIN_LOGIN, ADMIN_PASSWORD

basedir = os.path.abspath(os.path.dirname(__file__))
DATABASE_URL = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')


async def init_db(db_url, create_db: bool = False, schemas: bool = False) -> None:
    await Tortoise.init(
        db_url=db_url, modules={"models": ["model.models"]}, _create_db=create_db
    )


async def init(db_url: str = DATABASE_URL):
    await init_db(db_url, True, True)


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def client():
    async with AsyncClient(app=app_factory(), base_url="http://test") as client:
        await app_startup()
        yield client


@pytest.fixture(scope="session", autouse=True)
async def initialize_tests():
    await init()
    yield
    await Tortoise._drop_databases()


token: str


@pytest.mark.anyio
async def test_create_user(client: AsyncClient):
    response = await client.post(
        "/api/user/token",
        data={"username": ADMIN_LOGIN, "password": ADMIN_PASSWORD},
        headers={"content-type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200, response.text
    global token
    token = response.json()['access_token']


@pytest.mark.anyio
async def test_post_cargo_rate(client: AsyncClient):
    example_data = {
        "2020-06-01": [
            {
                "cargo_type": "Glass",
                "rate": 0.04
            },
            {
                "cargo_type": "Other",
                "rate": 0.01
            }
        ],
        "2020-07-01": [
            {
                "cargo_type": "Glass",
                "rate": 0.035
            },
            {
                "cargo_type": "Other",
                "rate": 0.015
            }
        ]
    }
    response = await client.post('/api/cargo',
                                 content=json.dumps(example_data),
                                 headers={'Authorization': f'Bearer {token}'}, )
    assert response.status_code == 200, example_data


@pytest.mark.anyio
async def test_get_cargo_types(client: AsyncClient):
    response = await client.get('/api/cargo/type')
    expected_json = {
        "cargo_types": [{
            "id": 1,
            "name": "Glass",
            "rates": [
                {
                    "id": 1,
                    "date": "2020-06-01",
                    "rate": 0.04
                },
                {
                    "id": 3,
                    "date": "2020-07-01",
                    "rate": 0.035
                }
            ]
        },
            {
                "id": 2,
                "name": "Other",
                "rates": [
                    {
                        "id": 2,
                        "date": "2020-06-01",
                        "rate": 0.01
                    },
                    {
                        "id": 4,
                        "date": "2020-07-01",
                        "rate": 0.015
                    }
                ]
            }],
        "count": 2
    }
    assert response.json() == expected_json, response.json()


@pytest.mark.anyio
async def test_get_calculate(client: AsyncClient):
    response = await client.get('/api/cargo/calculate?price=100&cargo_type_id=1&date=2020-06-01')
    assert response.json()['insurance'] == 4, response.json()
    response = await client.get('/api/cargo/calculate?price=100&cargo_type_id=1&date=2020-07-01')
    assert response.json()['insurance'] == 3.5, response.json()
    response = await client.get('/api/cargo/calculate?price=100&cargo_type_id=1&date=2020-05-01')
    assert response.status_code == 400, response.text
