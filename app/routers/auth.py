from fastapi import APIRouter, Depends, status, Request
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.schemas.auth import RegisterUser, LoginUser
from app.services.auth import register_user_service, login_user_service
from app.schemas.response import BaseResponseSchema

auth_router = APIRouter(prefix='/auth', tags=['Auth'])

@auth_router.post('/register', status_code=status.HTTP_201_CREATED, response_model=BaseResponseSchema)
def register_user(request: Request, new_user: RegisterUser, db: Session = Depends(get_db)):
    data = register_user_service(new_user, db)
    return BaseResponseSchema(
        status_code=status.HTTP_201_CREATED,
        message='Đăng ký tài khoản thành công',
        data=data,
        path=request.url.path
    )
    
@auth_router.post("/login", status_code=status.HTTP_200_OK, response_model=BaseResponseSchema)
def login_user(request: Request, credentials: LoginUser, db: Session = Depends(get_db)):
    data = login_user_service(credentials, db)
    return BaseResponseSchema(
        status_code=status.HTTP_200_OK,
        message="Đăng nhập thành công",
        data=data,
        path=request.url.path,
    )
