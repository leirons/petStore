from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import UnmappedInstanceError

from app.services.user import schemes

from core.auth import AuthHandler

from sqlalchemy import select
from core.repository.base import BaseRepo
from core.exceptions.user import UserExists


class UserLogic(BaseRepo):
    def __init__(self, model):
        self.auth_handler = AuthHandler()
        super(UserLogic, self).__init__(model)

    async def get_user_by_id(self, db: Session, user_id: int):
        query = select(self.model).where(self.model.id == user_id)
        r = await db.execute(query)
        return r.scalars().first()

    async def get_user_by_email(self, db: Session, email: str):
        query = select(self.model).where(self.model.email == email)
        r = await db.execute(query)
        return r.scalars().first()

    async def get_user_by_login(self, db: Session, login: str):
        query = select(self.model).where(self.model.login == login)
        r = await db.execute(query)
        return r.scalars().first()

    async def delete_user(self, db: Session, user_id: int):
        record = select(self.model).where(self.model.User.id == user_id)
        record = await db.execute(record)
        record = record.scalars().first()
        try:
            await db.delete(record)
            await db.commit()
        except UnmappedInstanceError as exc:
            return {'status_code': 404, 'detail': "Не удалось удалить пользователя"}
        return {'status_code': 200, "detail": "Пользователь удален"}

    async def create_user(self, password: str, db: Session, user: schemes.UserCreate):
        try:
            if await self.check_login(user.login, db) or await self.check_email(user.email, db):
                return False, UserExists
            hashed_password = self.auth_handler.get_passwords_hash(password)
            data = user.dict()
            data['password'] = hashed_password
            db_user = self.model(**data)
            db.add(db_user)

            await db.commit()
            await db.refresh(db_user)

        except Exception as exc:
            print(exc)
            return {'status_code': 500, "detail": "Не удалось создать пользователя"}
        return True, user

    async def check_login(self, login: str, db: Session):
        if await self.get_user_by_login(db, login):
            return True
        return False

    async def check_email(self, email: str, db: Session):
        if await self.get_user_by_email(db, email):
            return True
        return False

    async def patch_user(self, db: Session, user: schemes.UserPatch, user_id: int):

        try:
            db_user = select(self.model.User).filter(self.model.User.id == user_id)
            db_user = await db.execute(db_user)
            db_user = db_user.scalars().first()
            res = await self.check_login(login=user.login, db=db)
            if res:
                return res
            if user.login is not None:
                db_user.login = user.login
            if user.password is not None:
                hashed_password = self.auth_handler.get_passwords_hash(user.password)
                db_user.hash_password = hashed_password
            await db.commit()
            await db.refresh(db_user)
        except Exception as exc:
            print(exc)
            return {'status_code': 500, "detail": "Не удалось сделать обновить пользователя"}
        return {'status_code': 200, "detail": "Операция произведена успешно"}
