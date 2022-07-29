from sqlalchemy import select, String
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
            return {'status_code': 500, "detail": f"Не удалось создать питомца"}
        return {"pet": db_pet}

    async def find_by_status(self, db,status:str):
        query = select(self.model).where(self.model.status == status)
        r = await db.execute(query)
        return r.scalars().all()

    async def find_by_tags(self, db: Session, tags: list):
        lst = []
        for tag in tags:
            query = select(self.model).where(self.model.tags['name'].astext.cast(String) == tag)
            r = await db.execute(query)
            lst.extend(r.scalars().all())
        return [i.__dict__ for i in lst]
