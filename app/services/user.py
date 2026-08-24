from sqlalchemy.orm import Session
from app.models.user import User

def get_all_user_service(db: Session):
    return db.query(User).filter(User.role == "USER").all()