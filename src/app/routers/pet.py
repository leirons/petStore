from typing import List

from sqlalchemy.orm import Session

from app.schemes import Message
from app.services.pet import schemes
from app.services.pet.logic import PetLogic
from app.services.pet.models import Pet
from app.services.user.logic import UserLogic
from app.services.user.models import Users
from core import auth
from core.cache.backend import RedisBackend
from core.cache.cache import CacheManager
from core.cache.key_marker import CustomKeyMaker
from core.db.sessions import get_db
from core.exceptions.pet import PetAlreadyExists, PetDoesNotFound
from core.exceptions.user import UserDoesNotExists
from fastapi import APIRouter, Depends, HTTPException, Query, status

cache_manager = CacheManager(backend=RedisBackend(), key_maker=CustomKeyMaker())
router = APIRouter()
logic = PetLogic(model=Pet)
user_logic = UserLogic(model=Users)

auth_handler = auth.AuthHandler()


@cache_manager.cached(prefix="get_pet_list")
@router.get(
    "/pet/pet_list",
    tags=["pet"],
    name="Get list of all pets",
    status_code=status.HTTP_200_OK,
    response_model=List[schemes.PetBase],
    response_model_exclude={"category":{"id"}}
)
async def get_list(
    db: Session = Depends(get_db), user=Depends(auth_handler.auth_wrapper)
):
    pets = await logic.get_all(session=db)
    lst_ = []
    if not pets:
        return lst_
    for pet in pets:
        lst_.append(pet.__dict__)
    return lst_


@router.get(
    "/pet/find_by_status",
    tags=["pet"],
    response_model=List[schemes.PetBase],
    status_code=status.HTTP_200_OK,
    response_model_exclude={"category": {"id"}}
)
async def find_by_status(
    status: str = Query(
        examples={
            "available": {
                "name": "available",
            },
            "pending": {
                "name": "pending",
            },
            "sold": {
                "name": "sold",
            },
        },
        default="available",
    ),
    db: Session = Depends(get_db),
    user=Depends(auth_handler.auth_wrapper),
):
    res = await logic.find_by_status(status=status, db=db)
    lst_ = []
    for d in res:
        lst_.append(d.__dict__)
    return lst_


@router.post(
    "/pet",
    tags=["pet"],
    name="Add new pet to the store",
    status_code=status.HTTP_201_CREATED,
    responses={409: {"model": Message}, 404: {"model": Message}},
)
async def create_pet(
    pet: schemes.PetBase,
    db: Session = Depends(get_db),
    user=Depends(auth_handler.auth_wrapper),
):
    r = await logic.get_by_id(id=pet.id, session=db)
    if r:
        raise HTTPException(
            status_code=PetAlreadyExists.code, detail=PetAlreadyExists.message
        )

    if not await user_logic.get_by_id(id=pet.user_id, session=db):
        raise HTTPException(
            status_code=UserDoesNotExists.code, detail=UserDoesNotExists.message
        )

    pet = await logic.create_pet(pet=pet, db=db)
    return pet


@router.get(
    "/pet/{pet_id}",
    tags=["pet"],
    name="Finds Pets by id",
    response_model=schemes.PetBase,
    responses={
        409: {"model": Message},
    },
    response_model_exclude={"category": {"id"}}
)
async def find_by_id(
    pet_id: int, db: Session = Depends(get_db), user=Depends(auth_handler.auth_wrapper)
):
    pet = await logic.get_by_id(session=db, id=pet_id)
    if not pet:
        raise HTTPException(
            status_code=PetDoesNotFound.code, detail=PetDoesNotFound.message
        )
    return pet.__dict__


@router.delete(
    "/pet/{pet_id}",
    tags=["pet"],
    name="Delete Pets by id",
    status_code=200,
    responses={404: {"model": Message}},
)
async def delete_by_id(
    pet_id: int, db: Session = Depends(get_db), user=Depends(auth_handler.auth_wrapper)
):
    pet = await logic.get_by_id(id=pet_id, session=db)

    if not pet:
        raise HTTPException(
            status_code=PetDoesNotFound.code, detail=PetDoesNotFound.message
        )

    await logic.delete_by_id(id=pet_id, session=db)


@router.put(
    "/pet/{pet_id}",
    tags=["pet"],
    name="Update an existing pet",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=schemes.PetPut,
    responses={409: {"model": Message}, 404: {"model": Message}},
    response_model_exclude={"category": {"id"}}
)
async def update_pet(
    pet_id: int,
    pet: schemes.PetPut,
    db: Session = Depends(get_db),
    user=Depends(auth_handler.auth_wrapper),
):
    p = await logic.get_by_id(id=pet_id, session=db)

    if not p:
        raise HTTPException(
            status_code=PetDoesNotFound.code, detail=PetDoesNotFound.message
        )

    if not await user_logic.get_by_id(id=pet.user_id, session=db):
        raise HTTPException(
            status_code=UserDoesNotExists.code, detail=UserDoesNotExists.message
        )

    await logic.update_by_id(id=pet_id, params=pet.dict(), session=db)
    return pet
