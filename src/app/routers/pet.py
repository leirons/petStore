from typing import Union, List

from fastapi import (
    APIRouter,
    Depends,
    HTTPException, Query
)

from sqlalchemy.orm import Session
from app.services.pet.models import Pet
from app.services.pet import schemes
from app.services.pet.logic import PetLogic

from core import auth
from core.db.sessions import get_db
from core.exceptions.pet import PetDoesNotExists, PetAlreadyexists

router = APIRouter()
logic = PetLogic(model=Pet)
auth_handler = auth.AuthHandler()


@router.get("/pet/find_by_status", tags=['Pet'], response_model=List[schemes.PetBase])
async def find_by_status(status: str = Query(examples={
    "available": {
        "name": "available",
    },
    "pending": {
        "name": "pending",
    },
    "sold": {
        "name": "sold",
    }
}, default="available"), db: Session = Depends(get_db)):
    res = await logic.find_by_status(status=status, db=db)
    lst_ = []
    for d in res:
        lst_.append(d.__dict__)
    return lst_


@router.get("/pet/find_by_tag", tags=['Pet'], name="Finds Pets by tag", response_model=schemes.PetBase)
async def find_by_tag(tags: Union[List[str], None] = Query(default=None),
                      db: Session = Depends(get_db)):
    res = await logic.find_by_tags(tags=tags, db=db)
    return res


@router.post("/pet/", tags=['Pet'], name="Add new pet to the store")
async def create_pet(pet: schemes.PetBase, db: Session = Depends(get_db)):
    r = await logic.get_by_id(id=pet.id, session=db)
    if not r:
        pet = await logic.create_pet(pet=pet, db=db)
        return pet
    raise HTTPException(status_code=PetAlreadyexists.code, detail=PetAlreadyexists.message)


@router.get("/pet/{pet_id}", tags=['Pet'], name="Finds Pets by id", response_model=schemes.PetBase)
async def find_by_id(pet_id: int, db: Session = Depends(get_db)):
    pet = await logic.get_by_id(session=db, id=pet_id)
    if not pet:
        raise HTTPException(status_code=PetDoesNotExists.code, detail=PetDoesNotExists.message)
    return pet.__dict__


@router.delete("/pet/{pet_id}", tags=['Pet'], name="Delete Pets by id", status_code=200)
async def delete_by_id(pet_id: int, db: Session = Depends(get_db)):
    pet = await logic.get_by_id(id=pet_id, session=db)
    if not pet:
        raise HTTPException(status_code=PetDoesNotExists.code, detail=PetDoesNotExists.message)
    await logic.delete_by_id(id=pet_id, session=db)


@router.put("/pet/{pet_id}", tags=['Pet'], name="Update an existing pet", status_code=200)
async def update_pet(pet_id: int, pet: schemes.PetBase, db: Session = Depends(get_db)):
    p = await logic.get_by_id(id=pet_id, session=db)
    if not p:
        raise HTTPException(status_code=PetDoesNotExists.code, detail=PetDoesNotExists.message)
    await logic.update_by_id(id=pet.id, params=pet.dict(), session=db)
