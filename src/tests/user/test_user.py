import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.anyio


class TestCase:
    @pytest.mark.asyncio
    async def test_create_user_1(self, client: AsyncClient):
        data = {
            "email": "string5@gmail.com",
            "first_name": "Ivan",
            "last_name": "Grechka",
            "phone": "380502906562",
            "password": "string3004",
            "login": "string55",
        }
        response = await client.post("api/v1/user", json=data)
        assert response.status_code == 201

    @pytest.mark.asyncio
    async def test_create_user_2(self, client: AsyncClient):
        data = {
            "email": "string5gmail.com",
            "first_name": "Ivan",
            "last_name": "Grechka",
            "phone": "380502906562",
            "password": "string3004",
            "login": "string55",
        }
        response = await client.post("api/v1/user", json=data)
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_create_user_3(self, client: AsyncClient):
        data = {
            "email": "string@gmail.com",
            "first_name": "Ivan",
            "last_name": "Grechka",
            "phone": "380502906562",
            "password": "string",
            "login": "string55",
        }
        response = await client.post("api/v1/user", json=data)
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_create_user_4(self, client: AsyncClient):
        data = {
            "email": "string@gmail.com",
            "first_name": "Ivan",
            "last_name": "Grechka",
            "phone": "380502906562",
            "password": "stringasdasdsa",
            "login": "stri",
        }
        response = await client.post("api/v1/user", json=data)
        assert response.status_code == 201

    @pytest.mark.asyncio
    async def test_delete_user(self, client: AsyncClient):
        data = {
            "email": "string5@gmail.com",
            "first_name": "Ivan",
            "last_name": "Grechka",
            "phone": "380502906562",
            "password": "string3004",
            "username": "string55",
        }
        response = await client.post("api/v1/user", json=data)
        assert response.status_code == 201
        response = await client.delete("api/v1/user/string55")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_delete_user_2(self, client: AsyncClient):
        data = {
            "email": "string5@gmail.com",
            "first_name": "Ivan",
            "last_name": "Grechka",
            "phone": "380502906562",
            "password": "string3004",
            "login": "string55",
        }
        response = await client.post("api/v1/user", json=data)
        assert response.status_code == 201
        response = await client.delete("api/v1/user/string")
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_login(self, client: AsyncClient):
        data = {
            "email": "string5@gmail.com",
            "first_name": "Ivan",
            "last_name": "Grechka",
            "phone": "380502906562",
            "password": "string3004",
            "login": "string55",
        }
        response = await client.post("api/v1/user", json=data)
        assert response.status_code == 201
        login_data = {"login": "string55", "password": "string3004"}
        response = await client.post("api/v1/user/login", json=login_data)
        assert response.status_code == 200
