from app.db.database import Base, engine, get_db
from fastapi import FastAPI, status, Request, Depends
from app.schemas.response import ResponseSchema
from app.core.exceptions import register_exception_handlers
from app.routers.auth import auth_router
from app.routers.users import user_router
from app.routers.event import event_router
from app.routers.event_staff import event_staff_router
from app.routers.event_task import event_task_router
from app.models.event import Event
from app.models.event_staff import EventStaff
from app.models.event_task import EventTask
from app.models.user import User
from sqlalchemy.orm import Session
from app.services.user import count_users_in_db

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Event Management API")

register_exception_handlers(app)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(event_router)
app.include_router(event_staff_router)
app.include_router(event_task_router)

@app.get("/health", response_model=ResponseSchema, tags=["Health"])
def health_check(request: Request, db: Session = Depends(get_db)):
    return ResponseSchema(
        status_code=status.HTTP_200_OK,
        message="Server đang hoạt động bình thường!",
        data={"status": "healthy", "total_users": count_users_in_db(db)},
        errors=None,
        path=request.url.path,
    )