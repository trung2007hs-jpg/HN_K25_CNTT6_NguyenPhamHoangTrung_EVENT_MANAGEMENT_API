from app.schemas.auth import RegisterUser, LoginUser
from sqlalchemy.orm import Session
from app.models.user import User
from fastapi import HTTPException, status
from app.core.security import hash_password, verify_password, create_access_token

def register_user_service(user: RegisterUser, db: Session):
    check_exist_email = db.query(User).filter(User.email == user.email).first()
    if check_exist_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Email is exist'
        )
    new_user = User(
        email=user.email,
        password_hash=hash_password(user.password),
        full_name=user.full_name.lower().title()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
    
def login_user_service(credentials: LoginUser, db: Session):
    user = db.query(User).filter(User.email == credentials.email).first()

    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email hoặc mật khẩu không chính xác",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tài khoản này đã bị khóa",
        )

    access_token = create_access_token(data={"sub": user.email, "role": user.role})
    return {
        "access_token": access_token, 
        "token_type": "bearer"
    }