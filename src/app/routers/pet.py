from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.schemes import Message
from app.services.pet import schemes
from app.services.pet.logic import PetLogic
from app.services.pet.models import Pet
from app.services.user.logic import UserLogic
from app.services.user.models import Users
from app.utils import object_as_dict
from core import auth
from core.cache.backend import RedisBackend
from core.cache.cache import CacheManager
from core.cache.key_marker import CustomKeyMaker
from core.db.sessions import get_db
from core.exceptions.pet import PetAlreadyExists, PetDoesNotFound
from core.exceptions.user import UserDoesNotExists

cache_manager = CacheManager(backend=RedisBackend(), key_maker=CustomKeyMaker())
router = APIRouter()
logic = PetLogic(model=Pet)
user_logic = UserLogic(model=Users)

auth_handler = auth.AuthHandler()


@router.get(
    "/pet/find_by_tag",
    tags=["pet"],
    response_model=List[schemes.PetBase],
    status_code=status.HTTP_200_OK,
    response_model_exclude={"category": {"id"}}
)
async def find_by_tag(
        db: Session = Depends(get_db),
        user=Depends(auth_handler.auth_wrapper),
        tag: str = None
):
    res = await logic.find_by_tag(tag=tag, db=db)
    lst_ = []
    tags = []
    for pet in res:
        for tag in pet.tag:
            tags.append(object_as_dict(tag))
        pet = pet.__dict__
        pet['tag'] = tags
        lst_.append(pet)
        tags = []
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
    tags = []
    for pet in res:
        for tag in pet.tag:
            tags.append(object_as_dict(tag))
        pet = pet.__dict__
        pet['tag'] = tags
        lst_.append(pet)
        tags = []
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

    p = await logic.create_pet(pet=pet, db=db)
    return p


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
    pet = await logic.get_pet_by_id(db=db, pet_id=pet_id)

    if not pet:
        raise HTTPException(
            status_code=PetDoesNotFound.code, detail=PetDoesNotFound.message
        )

    tags = []
    for tag in pet.tag:
        tags.append(object_as_dict(tag))
    pet = pet.__dict__
    pet['tag'] = tags
    return pet


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

    await logic.update_by_id(id=pet_id, pet=pet, db=db)
    return pet
