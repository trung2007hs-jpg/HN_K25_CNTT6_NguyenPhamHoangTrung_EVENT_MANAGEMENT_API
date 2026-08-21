from app.dependencies.auth import get_current_user, get_current_admin
from app.models.user import User
from app.schemas.response import ResponseSchema
from app.schemas.user import UserResponse
from fastapi import APIRouter, Depends, Request, status, HTTPException
from app.services.user import get_all_user_service
from sqlalchemy.orm import Session
from app.db.database import get_db

user_router = APIRouter(prefix="/users", tags=["Users"])

@user_router.get("/me", response_model=ResponseSchema[dict])
def get_me(request: Request, current_user: User = Depends(get_current_user)):
    return ResponseSchema(
        status_code=status.HTTP_200_OK,
        message="Lấy thông tin tài khoản thành công",
        data={
            "email": current_user.email,
            "full_name": current_user.full_name,
            "role": current_user.role,
        },
        path=request.url.path,
    )
    
@user_router.get("/", response_model=ResponseSchema[list[UserResponse]])
def get_all_users(request: Request, current_user: User = Depends(get_current_admin), db: Session=Depends(get_db)):
    data = get_all_user_service(db)
    return ResponseSchema(
        status_code=status.HTTP_200_OK,
        message="Lấy danh sách tài khoản thành công",
        data=data,
        path=request.url.path,
    )
