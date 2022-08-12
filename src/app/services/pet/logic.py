from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session, selectinload

from app.services.pet import schemes
from app.services.pet.models import Tag
from core.exceptions.server import ServerError
from core.repository.base import BaseRepo


class PetLogic(BaseRepo):
    def __init__(self, model):
        super(PetLogic, self).__init__(model)

    async def get_or_create(self, session, model, tag):
        query = select(model).filter_by(**tag)
        res = await session.execute(query)
        instance = res.scalars().first()
        if instance:
            return instance
        else:
            instance = model(**tag)
            session.add(instance)
            await session.commit()
            await session.refresh(instance)
            return instance

    async def create_pet(self, db: Session, pet: schemes.PetBase):

        instance_pet = pet.dict()
        instance_pet.pop("tag")
        try:
            db_pet = self.model(**instance_pet)
            db.add(db_pet)

            await db.commit()
            await db.refresh(db_pet)

        except Exception:
            return {"status_code": ServerError.error_code, "detail": ServerError.message}

        for tag in pet.tag:
            tag = tag.dict()
            tag['pet_id'] = pet.id
            await self.get_or_create(session=db, model=Tag, tag=tag)

        return {"pet": pet.dict()}

    async def delete_tags(self, pet_id, session):
        query = delete(Tag).where(Tag.pet_id == pet_id)
        await session.execute(query)
        await session.commit()

    async def find_by_status(self, db, status: str):
        query = select(
            self.model,
            Tag,
        ).filter(
            Tag.pet_id == self.model.id
        ).filter(
            self.model.status == status
        ).options(selectinload(self.model.tag))
        res = await db.execute(query)
        instances = res.scalars().all()
        return instances

    async def find_by_tag(self, db, tag):
        query = select(
            self.model,
            Tag,
        ).filter(
            Tag.name == tag
        ).filter(self.model.id == Tag.pet_id).options(selectinload(self.model.tag))
        res = await db.execute(query)
        instances = res.scalars().all()
        return instances

    async def update_by_id(self, id: int, pet: schemes.PetPut, db) -> None:
        await self.delete_tags(pet_id=id, session=db)
        for tag in pet.tag:
            tag = tag.dict()
            tag['pet_id'] = id
            await self.get_or_create(session=db, model=Tag, tag=tag)

        instance_pet = pet.dict()
        instance_pet.pop("tag")
        query = update(self.model).where(self.model.id == id).values(**instance_pet)
        await db.execute(query)
        await db.commit()

    async def get_pet_by_id(self, db, pet_id):
        query = select(
            self.model,
            Tag,
        ).filter(
            self.model.id == pet_id
        ).options(selectinload(self.model.tag))
        res = await db.execute(query)
        instance = res.scalars().first()
        return instance
