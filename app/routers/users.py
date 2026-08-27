from app.dependencies.auth import get_current_user, get_current_admin, get_current_manager
from app.models.user import User
from app.schemas.response import ResponseSchema
from app.schemas.user import UserResponse
from fastapi import APIRouter, Depends, Query, Request, status, HTTPException
from app.services.user import get_all_user_service, calculate_days_from_creation
from sqlalchemy.orm import Session
from app.db.database import get_db
from typing import Optional
from app.schemas.user import SearchUser

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
            'is_admin': True if current_user.role == 'ADMIN' else False,
            'account_age_days': f'{calculate_days_from_creation(current_user)} days'
        },
        path=request.url.path,
    )
    
@user_router.get("/", response_model=ResponseSchema[list[UserResponse]])
def get_all_users(
    request: Request, 
    keyword: Optional[str] = None, 
    current_user: User = Depends(get_current_manager), 
    db: Session=Depends(get_db), 
    search: Optional[SearchUser] = None, 
    is_active: Optional[bool] = None,
    domain: Optional[str] = Query(default=None, min_length=1),
):
    data = get_all_user_service(
        db=db,
        keyword=keyword,
        search=search,
        is_active=is_active,
        domain=domain,
    )
    return ResponseSchema(
        status_code=status.HTTP_200_OK,
        message="Lấy danh sách tài khoản thành công",
        data=data,
        path=request.url.path,
    )
