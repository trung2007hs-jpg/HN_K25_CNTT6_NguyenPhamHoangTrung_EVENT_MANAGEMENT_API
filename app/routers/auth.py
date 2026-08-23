from datetime import datetime
from fastapi import APIRouter, Depends, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.schemas.auth import RegisterUser, LoginUser
from app.schemas.user import UserBase
from app.services.auth import register_user_service, login_user_service
from app.schemas.response import BaseResponseSchema, TokenData

auth_router = APIRouter(prefix='/auth', tags=['Auth'])

@auth_router.post('/register', status_code=status.HTTP_201_CREATED, response_model=BaseResponseSchema[UserBase])
def register_user(request: Request, new_user: RegisterUser, db: Session = Depends(get_db)):
    data = register_user_service(new_user, db)
    return BaseResponseSchema(
        status_code=status.HTTP_201_CREATED,
        message='Đăng ký tài khoản thành công',
        data=data,
        path=request.url.path
    )
    
@auth_router.post("/login", response_model=TokenData)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    credentials = LoginUser(
        email=form_data.username,
        password=form_data.password,
    )
    data = login_user_service(credentials, db)
    return TokenData(
        access_token=data["access_token"],
        token_type=data["token_type"],
    )
