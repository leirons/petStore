import pytest
from httpx import AsyncClient

from app.services.user.logic import UserLogic
from app.services.user.models import Users
from app.services.user.schemes import UserCreate

pytestmark = pytest.mark.anyio


class TestCase:
    @pytest.mark.asyncio
    async def test_create_pet(self, client: AsyncClient, get_session):
        data = {
            "email": "string5@gmail.com",
            "first_name": "Ivan",
            "last_name": "Grechka",
            "phone": "380502906562",
            "password": "string3004",
            "login": "string55",
        }
        data = UserCreate(**data)
        user_logic = UserLogic(Users)

        res = await user_logic.create_user(password=data.password, user=data, db=get_session)
        print(res)
        pet_data = {
            "id": 0,
            "user_id": 1,
            "name": "doggie",
            "category": {"id": 0, "name": " Dogs"},
            "status": "available",
            "tag": [
                {
                    "name": "Tag"
                }
            ]
        }
        login_data = {
            "login": "string55",
            "password": 'string3004'
        }
        response = await client.post("api/v1/user/login", json=login_data)
        assert response.status_code == 200

        headers = {}
        headers['Authorization'] = f"Bearer {response.json().get('token')}"
        response = await client.post("api/v1/pet", json=pet_data, headers=headers)
        assert response.status_code == 201

    @pytest.mark.asyncio
    async def test_delete_pet(self, client: AsyncClient, get_session):
        data = {
            "email": "string5@gmail.com",
            "first_name": "Ivan",
            "last_name": "Grechka",
            "phone": "380502906562",
            "password": "string3004",
            "login": "string55",
        }
        data = UserCreate(**data)
        user_logic = UserLogic(Users)

        await user_logic.create_user(password=data.password, user=data, db=get_session)

        pet_data = {
            "id": 0,
            "user_id": 1,
            "name": "doggie",
            "category": {"id": 0, "name": " Dogs"},
            "status": "available",
            "tag": [
                {
                    "name": "Tag"
                }
            ]
        }
        login_data = {
            "login": "string55",
            "password": 'string3004'
        }
        response = await client.post("api/v1/user/login", json=login_data)
        assert response.status_code == 200

        headers = {}
        headers['Authorization'] = f"Bearer {response.json().get('token')}"

        response = await client.post("api/v1/pet", json=pet_data, headers=headers)
        assert response.status_code == 201

        response = await client.delete("api/v1/pet/0", headers=headers)
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_get_pet(self, client: AsyncClient, get_session):
        data = {
            "email": "string5@gmail.com",
            "first_name": "Ivan",
            "last_name": "Grechka",
            "phone": "380502906562",
            "password": "string3004",
            "login": "string55",
        }
        data = UserCreate(**data)
        user_logic = UserLogic(Users)

        await user_logic.create_user(password=data.password, user=data, db=get_session)

        pet_data = {
            "id": 0,
            "user_id": 1,
            "name": "doggie",
            "category": {"id": 0, "name": " Dogs"},
            "status": "available",
            "tag": [
                {
                    "name": "Tag"
                }
            ]
        }
        login_data = {
            "login": "string55",
            "password": 'string3004'
        }
        response = await client.post("api/v1/user/login", json=login_data)
        assert response.status_code == 200

        headers = {}
        headers['Authorization'] = f"Bearer {response.json().get('token')}"

        response = await client.post("api/v1/pet", json=pet_data, headers=headers)
        assert response.status_code == 201

        response = await client.get("api/v1/pet/0", headers=headers)
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_get_pet_by_status(self, client: AsyncClient, get_session):
        data = {
            "email": "string5@gmail.com",
            "first_name": "Ivan",
            "last_name": "Grechka",
            "phone": "380502906562",
            "password": "string3004",
            "login": "string55",
        }
        data = UserCreate(**data)
        user_logic = UserLogic(Users)

        await user_logic.create_user(password=data.password, user=data, db=get_session)

        pet_data = {
            "id": 0,
            "user_id": 1,
            "name": "doggie",
            "category": {"id": 0, "name": " Dogs"},
            "status": "available",
            "tag": [
                {
                    "name": "Tag"
                }
            ]
        }

        login_data = {
            "login": "string55",
            "password": 'string3004'
        }
        response = await client.post("api/v1/user/login", json=login_data)
        assert response.status_code == 200

        headers = {}
        headers['Authorization'] = f"Bearer {response.json().get('token')}"

        response = await client.post("api/v1/pet", json=pet_data, headers=headers)
        assert response.status_code == 201

        response = await client.get("api/v1/pet/find_by_status?status=available",headers=headers)
        assert response.status_code == 200
        assert response.json()[0]["id"] == 0
        assert response.json()[0]["user_id"] == 1
        assert response.json()[0]["name"] == "doggie"
        assert response.json()[0]["status"] == "available"

    @pytest.mark.asyncio
    async def test_get_pet_by_status_2(self, client: AsyncClient, get_session):
        data = {
            "email": "string5@gmail.com",
            "first_name": "Ivan",
            "last_name": "Grechka",
            "phone": "380502906562",
            "password": "string3004",
            "login": "string55",
        }
        data = UserCreate(**data)
        user_logic = UserLogic(Users)

        await user_logic.create_user(password=data.password, user=data, db=get_session)

        pet_data = {
            "id": 0,
            "user_id": 1,
            "name": "doggie",
            "category": {"id": 0, "name": " Dogs"},
            "status": "pending",
            "tag": [
                {
                    "name": "Tag"
                }
            ]
        }

        login_data = {
            "login": "string55",
            "password": 'string3004'
        }
        response = await client.post("api/v1/user/login", json=login_data)
        assert response.status_code == 200

        headers = {}
        headers['Authorization'] = f"Bearer {response.json().get('token')}"

        response = await client.post("api/v1/pet", json=pet_data, headers=headers)
        assert response.status_code == 201

        response = await client.get("api/v1/pet/find_by_status?status=pending", headers=headers)
        assert response.status_code == 200
        assert response.json()[0]["id"] == 0
        assert response.json()[0]["user_id"] == 1


    @pytest.mark.asyncio
    async def test_update_pet(self, client: AsyncClient, get_session):
        data = {
            "email": "string5@gmail.com",
            "first_name": "Ivan",
            "last_name": "Grechka",
            "phone": "380502906562",
            "password": "string3004",
            "login": "string55",
        }
        data = UserCreate(**data)
        user_logic = UserLogic(Users)

        await user_logic.create_user(password=data.password, user=data, db=get_session)

        pet_data = {
            "id": 0,
            "user_id": 1,
            "name": "doggie",
            "tags": {"id": 0, "name": "string"},
            "category": {"id": 0, "name": " Dogs"},
            "status": "pending",
            "tag": [
                {
                    "name": "Tag"
                }
            ]
        }

        login_data = {
            "login": "string55",
            "password": 'string3004'
        }
        response = await client.post("api/v1/user/login", json=login_data)
        assert response.status_code == 200

        headers = {}
        headers['Authorization'] = f"Bearer {response.json().get('token')}"

        response = await client.post("api/v1/pet", json=pet_data, headers=headers)
        assert response.status_code == 201

        pet_data["name"] = "cat"
        response = await client.put("api/v1/pet/0", json=pet_data,headers=headers)
        assert response.status_code == 202
        assert response.json()["name"] == "cat"

    @pytest.mark.asyncio
    async def test_update_pet_2(self, client: AsyncClient, get_session):
        data = {
            "email": "string5@gmail.com",
            "first_name": "Ivan",
            "last_name": "Grechka",
            "phone": "380502906562",
            "password": "string3004",
            "login": "string55",
        }
        data = UserCreate(**data)
        user_logic = UserLogic(Users)

        await user_logic.create_user(password=data.password, user=data, db=get_session)

        pet_data = {
            "id": 0,
            "user_id": 12312,
            "name": "doggie",
            "tags": {"id": 0, "name": "string"},
            "category": {"id": 0, "name": " Dogs"},
            "status": "pending",
            "tag": [
                {
                    "name": "Tag"
                }
            ]
        }
        login_data = {
            "login": "string55",
            "password": 'string3004'
        }
        response = await client.post("api/v1/user/login", json=login_data)
        assert response.status_code == 200

        headers = {}
        headers['Authorization'] = f"Bearer {response.json().get('token')}"

        response = await client.post("api/v1/pet", json=pet_data, headers=headers)
        assert response.status_code == 404
        assert response.json()["detail"] == "User does not exists"
