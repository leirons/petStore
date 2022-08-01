import pytest
from httpx import AsyncClient

from app.services.pet.logic import PetLogic
from app.services.pet.models import Pet
from app.services.pet.schemes import PetBase
from app.services.user.logic import UserLogic
from app.services.user.models import Users
from app.services.user.schemes import UserCreate

pytestmark = pytest.mark.anyio


class TestCase:
    @pytest.mark.asyncio
    async def test_create_order(self, client: AsyncClient, get_session):
        data = {
            "email": "string5@gmail.com",
            "first_name": "Ivan",
            "last_name": "Grechka",
            "phone": "380502906562",
            "password": "string3004",
            "login": "string55",
        }

        pet_data = {
            "id": 0,
            "user_id": 1,
            "name": "doggie",
            "tags": {"id": 0, "name": "string"},
            "category": {"id": 0, "name": " Dogs"},
            "status": "available",
        }
        user_data = UserCreate(**data)
        pet_data = PetBase(**pet_data)
        user_logic = UserLogic(Users)
        pet_logic = PetLogic(Pet)

        await user_logic.create_user(
            password=user_data.password, user=user_data, db=get_session
        )
        login_data = {
            "login": "string55",
            "password": 'string3004'
        }
        response = await client.post("api/v1/user/login", json=login_data)
        print(response.text)
        assert response.status_code == 200

        headers = {}
        headers['Authorization'] = f"Bearer {response.json().get('token')}"

        await pet_logic.create_pet(db=get_session, pet=pet_data)
        order = {
            "id": 5,
            "pet_id": 0,
            "quantity": 0,
            "status": "complete",
            "complete": True,
        }

        response = await client.post("api/v1/store", json=order,headers=headers)
        assert response.status_code == 201

    @pytest.mark.asyncio
    async def test_create_order_2(self, client: AsyncClient, get_session):
        data = {
            "email": "string5@gmail.com",
            "first_name": "Ivan",
            "last_name": "Grechka",
            "phone": "380502906562",
            "password": "string3004",
            "login": "string55",
        }

        pet_data = {
            "id": 0,
            "user_id": 1,
            "name": "doggie",
            "tags": {"id": 0, "name": "string"},
            "category": {"id": 0, "name": " Dogs"},
            "status": "available",
        }
        user_data = UserCreate(**data)
        pet_data = PetBase(**pet_data)
        user_logic = UserLogic(Users)
        pet_logic = PetLogic(Pet)

        await user_logic.create_user(
            password=user_data.password, user=user_data, db=get_session
        )
        await pet_logic.create_pet(db=get_session, pet=pet_data)
        order = {
            "id": 5,
            "pet_id": 1,
            "quantity": 0,
            "status": "complete",
            "complete": True,
        }
        login_data = {
            "login": "string55",
            "password": 'string3004'
        }
        response = await client.post("api/v1/user/login", json=login_data)
        print(response.text)
        assert response.status_code == 200

        headers = {}
        headers['Authorization'] = f"Bearer {response.json().get('token')}"

        response = await client.post("api/v1/store", json=order,headers=headers)
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_order(self, client: AsyncClient, get_session):
        data = {
            "email": "string5@gmail.com",
            "first_name": "Ivan",
            "last_name": "Grechka",
            "phone": "380502906562",
            "password": "string3004",
            "login": "string55",
        }

        pet_data = {
            "id": 0,
            "user_id": 1,
            "name": "doggie",
            "tags": {"id": 0, "name": "string"},
            "category": {"id": 0, "name": " Dogs"},
            "status": "available",
        }
        user_data = UserCreate(**data)
        pet_data = PetBase(**pet_data)
        user_logic = UserLogic(Users)
        pet_logic = PetLogic(Pet)

        await user_logic.create_user(
            password=user_data.password, user=user_data, db=get_session
        )
        await pet_logic.create_pet(db=get_session, pet=pet_data)
        order = {
            "id": 5,
            "pet_id": 0,
            "quantity": 0,
            "status": "complete",
            "complete": True,
        }

        login_data = {
            "login": "string55",
            "password": 'string3004'
        }
        response = await client.post("api/v1/user/login", json=login_data)
        print(response.text)
        assert response.status_code == 200

        headers = {}
        headers['Authorization'] = f"Bearer {response.json().get('token')}"


        response = await client.post("api/v1/store", json=order,headers=headers)
        assert response.status_code == 201

        response = await client.delete("api/v1/store/5",headers=headers)
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_get_order_by_id(self, client: AsyncClient, get_session):
        data = {
            "email": "string5@gmail.com",
            "first_name": "Ivan",
            "last_name": "Grechka",
            "phone": "380502906562",
            "password": "string3004",
            "login": "string55",
        }

        pet_data = {
            "id": 0,
            "user_id": 1,
            "name": "doggie",
            "tags": {"id": 0, "name": "string"},
            "category": {"id": 0, "name": " Dogs"},
            "status": "available",
        }
        user_data = UserCreate(**data)
        pet_data = PetBase(**pet_data)
        user_logic = UserLogic(Users)
        pet_logic = PetLogic(Pet)

        await user_logic.create_user(
            password=user_data.password, user=user_data, db=get_session
        )
        await pet_logic.create_pet(db=get_session, pet=pet_data)

        order = {
            "id": 5,
            "pet_id": 0,
            "quantity": 0,
            "status": "complete",
            "complete": True,
        }
        login_data = {
            "login": "string55",
            "password": 'string3004'
        }
        response = await client.post("api/v1/user/login", json=login_data)
        print(response.text)
        assert response.status_code == 200

        headers = {}
        headers['Authorization'] = f"Bearer {response.json().get('token')}"

        response = await client.post("api/v1/store", json=order,headers=headers)
        assert response.status_code == 201

        response = await client.get("api/v1/store/5",headers=headers)
        assert response.status_code == 200
        assert response.json()["id"] == 5
        assert response.json()["status"] == "complete"
