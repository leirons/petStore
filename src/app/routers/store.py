from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session
from app.services.store.models import Store
from app.services.store.logic import StoreLogic
from app.services.store import schemes

from core import auth
from core.db.sessions import get_db

router = APIRouter()
logic = StoreLogic(model=Store)
auth_handler = auth.AuthHandler()


@router.get("/order/inventory", tags=['Store'], name="Returns pet inventories by status")
async def find_by_id(db: Session = Depends(get_db)):
    res = await logic.get_inventory(db=db)
    return res


@router.post("/store/order", tags=['Store'], name="Place an order for pet")
async def create_pet(order: schemes.Order, db: Session = Depends(get_db)):
    status = order.status.lower()
    if status == "complete" or status == "approved" or status == "delivered":
        res = await logic.create_order(order=order, db=db)
        return res


@router.delete("/store/order/{order_id}", tags=['Store'], name="Delete Order by id", status_code=200)
async def delete_by_id(order_id: int, db: Session = Depends(get_db)):
    pet = await logic.get_by_id(id=order_id, session=db)
    if not pet:
        return "error"
    await logic.delete_by_id(id=order_id, session=db)
    return {"detail": "Success"}


@router.get("/order/{order_id}", tags=['Store'], name="Finds Order by id", response_model=schemes.Order)
async def find_by_id(order_id: int, db: Session = Depends(get_db)):
    res = await logic.get_by_id(session=db, id=order_id)
    if not res:
        pass
    return res.__dict__
