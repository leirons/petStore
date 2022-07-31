from sqlalchemy import select
from sqlalchemy.orm import Session

from app.services.pet import schemes
from core.repository.base import BaseRepo


class PetLogic(BaseRepo):
    def __init__(self, model):
        super(PetLogic, self).__init__(model)

    async def create_pet(self, db: Session, pet: schemes.PetBase):
        print(pet)
        try:
            db_pet = self.model(**pet.dict())
            db.add(db_pet)

            await db.commit()
            await db.refresh(db_pet)

        except Exception as exc:
            print(exc)
            return {"status_code": 500, "detail": f"Не удалось создать питомца"}
        return {"pet": db_pet}

    async def find_by_status(self, db, status: str):
        query = select(self.model).where(self.model.status == status)
        r = await db.execute(query)
        return r.scalars().all()
