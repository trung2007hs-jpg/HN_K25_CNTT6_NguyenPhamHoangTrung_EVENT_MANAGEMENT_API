from typing import Optional
from app.models.user import User
from app.schemas.user import SearchStatus, SearchUser
from sqlalchemy.orm import Session


def get_all_user_service(
    db: Session,
    keyword: Optional[str] = None,
    search: Optional[SearchUser] = None,
    is_active: Optional[SearchStatus] = None,
):
    query = db.query(User).filter(User.role == "USER")
    if keyword:
        if search == SearchUser.EMAIL:
            target_column = User.email
        elif search == SearchUser.FULL_NAME:
            target_column = User.full_name
        else:
            target_column = User.email

        query = query.filter(target_column.ilike(f"%{keyword}%"))
    if is_active is not None:
        active_value = 1 if is_active == SearchStatus.ACTIVE else 0
        query = query.filter(User.is_active == active_value)
    return query.all()