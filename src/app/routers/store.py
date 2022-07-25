from fastapi import (
    APIRouter,
    Depends, HTTPException
)

from sqlalchemy.orm import Session
from app.services.store.models import Store
from app.services.pet.models import Pet
from app.services.store.logic import StoreLogic
from app.services.pet.logic import PetLogic
from app.services.store import schemes

from core import auth
from core.db.sessions import get_db
from core.exceptions.pet import PetDoesNotExists
from core.exceptions.store import (
    OrderDoesNotExists,
    StatusDoesNotCorrect,
    OrderAlreadyExists
)

router = APIRouter()
logic = StoreLogic(model=Store)
pet_logic = PetLogic(model=Pet)
auth_handler = auth.AuthHandler()


@router.get("/order/inventory", tags=['Store'], name="Returns pet inventories by status")
async def find_by_id(db: Session = Depends(get_db)):
    res = await logic.get_inventory(db=db)
    return res


@router.post("/store/order", tags=['Store'], name="Place an order for pet")
async def create_pet(order: schemes.Order, db: Session = Depends(get_db)):
    order = await logic.get_by_id(id=order.id, session=db)
    if order:
        raise HTTPException(detail=OrderAlreadyExists.message, status_code=OrderAlreadyExists.error_code)
    status = order.status.lower()
    pet = await pet_logic.get_by_id(id=order.pet_id, session=db)
    if not pet:
        raise HTTPException(detail=PetDoesNotExists.message, status_code=PetDoesNotExists.error_code)

    if status != "complete" and status != "approved" and status != "delivered":
        raise HTTPException(detail=StatusDoesNotCorrect.message, status_code=StatusDoesNotCorrect.error_code)

    res = await logic.create_order(order=order, db=db)
    return res


@router.delete("/store/order/{order_id}", tags=['Store'], name="Delete Order by id", status_code=200)
async def delete_by_id(order_id: int, db: Session = Depends(get_db)):
    order = await logic.get_by_id(id=order_id, session=db)
    if not order:
        raise HTTPException(detail=OrderDoesNotExists.message, status_code=OrderDoesNotExists.error_code)
    await logic.delete_by_id(id=order_id, session=db)


@router.get("/order/{order_id}", tags=['Store'], name="Finds Order by id", response_model=schemes.Order)
async def find_by_id(order_id: int, db: Session = Depends(get_db)):
    order = await logic.get_by_id(session=db, id=order_id)
    if not order:
        raise HTTPException(detail=OrderDoesNotExists.message, status_code=OrderDoesNotExists.error_code)
    return order.__dict__
