from app.db.database import Base, engine
from fastapi import FastAPI, status, Request
from app.schemas.response import ResponseSchema
from app.core.exceptions import register_exception_handlers
from app.routers.auth import auth_router
from app.routers.users import user_router
from app.routers.event import event_router
from app.routers.event_staff import event_staff_router
from app.models.event import Event
from app.models.event_staff import EventStaff
from app.models.event_task import EventTask
from app.models.user import User

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Event Management API")

register_exception_handlers(app)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(event_router)
app.include_router(event_staff_router)

@app.get("/health", response_model=ResponseSchema, tags=["Health"])
def health_check(request: Request):
    return ResponseSchema(
        status_code=status.HTTP_200_OK,
        message="Server đang hoạt động bình thường!",
        data={"status": "healthy"},
        errors=None,
        path=request.url.path,
    )