from sqlalchemy import select
from sqlalchemy.orm import Session

from core.repository.base import BaseRepo


class StoreLogic(BaseRepo):
    def __init__(self, model):
        super(StoreLogic, self).__init__(model)

    async def create_order(self, order, db: Session):
        try:
            db_order = self.model(**order.dict())
            db.add(db_order)

            await db.commit()
            await db.refresh(db_order)

        except Exception:
            return {"status_code": 500, "detail": f"Не удалось создать заказ"}
        return {"order": db_order}

    async def get_inventory(self, db: Session):
        # TODO Make good query
        data = {
            "approved": 0,
            "complete": 0,
            "delivered": 0,
        }
        query = select(self.model)
        res = await db.execute(query)
        res = res.scalars().all()
        for i in res:
            data[i.status] += 1
        return data
