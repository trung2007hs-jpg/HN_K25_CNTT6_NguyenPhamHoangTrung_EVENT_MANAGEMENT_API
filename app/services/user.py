from typing import Optional
from app.models.user import User
from app.schemas.user import SearchUser
from sqlalchemy.orm import Session
from datetime import datetime


def get_all_user_service(
    db: Session,
    keyword: Optional[str] = None,
    search: Optional[SearchUser] = None,
    is_active: Optional[bool] = None,
    domain: Optional[str] = None,
):
    query = db.query(User).filter(User.role == "USER")
    if domain:
        query = query.filter(User.email.ilike(f"%@{domain.strip()}"))
    if keyword:
        if search == SearchUser.EMAIL:
            target_column = User.email
        elif search == SearchUser.FULL_NAME:
            target_column = User.full_name
        else:
            target_column = User.email

        query = query.filter(target_column.ilike(f"%{keyword}%"))
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    return query.all()

def count_users_in_db(db: Session):
    return db.query(User).count()

def calculate_days_from_creation(user: User) -> int:
    if user.created_at:
        current_date = datetime.now()
        days_difference = (current_date - user.created_at).days
        return days_difference
    return 0