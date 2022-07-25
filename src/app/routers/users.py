from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    Response,
)

from sqlalchemy.orm import Session
from app.services.user.models import User
from app.services.user import schemes
from app.services.user.logic import UserLogic

from core import auth
from core.db.sessions import get_db

router = APIRouter()
logic = UserLogic(model=User)
auth_handler = auth.AuthHandler()


@router.post("/user", tags=['User'])
async def create_user(user: schemes.UserCreate, db: Session = Depends(get_db)):
    operation, res = await logic.create_user(db=db, user=user, password=user.password)
    if not operation:
        return HTTPException(detail=res.message, status_code=res.code)
    return res


@router.post("/user/login", tags=['User'])
async def login(user: schemes.UserToken, db: Session = Depends(get_db)):
    user_old = await logic.get_user_by_login(db, user.login)
    if user_old and auth_handler.verify_password(plain_password=user.password, hash_password=user_old.password):
        token = auth_handler.encode_token(user_old.id)
        return {"token": token}
    return HTTPException(status_code=400, detail="Does not correct login or password")


@router.delete("/user/{user_id}", tags=["User"])
async def delete_user(request: Request, db: Session = Depends(get_db),
                      user=Depends(auth_handler.auth_wrapper)):
    res = await logic.delete_user(db, user_id=request.user.id)
    return res


@router.get("/user/", response_model=schemes.User, tags=["User"])
async def get_myself(request: Request, user=Depends(auth_handler.auth_wrapper), db: Session = Depends(get_db)):
    res = await logic.get_user_by_id(db, user_id=request.user.id)
    return res


@router.patch('/user/{user_id}', tags=['User'])
async def patch_user(request: Request, user: schemes.UserPatch, db: Session = Depends(get_db),
                     user_auth=Depends(auth_handler.auth_wrapper)):
    res = await logic.patch_user(db=db, user=user, user_id=request.user.id)
    return res


@router.get('/user/logout', tags=['User'])
async def user_logout(request: Request,response:Response):
    print('1')
    print(1/0)
