from app.db.database import Base, engine
from fastapi import FastAPI, status, Request
from schemas.response import ResponseSchema
from app.core.exceptions import register_exception_handlers

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Event Management API")

register_exception_handlers(app)

@app.get("/health", response_model=ResponseSchema, tags=["Health"])
def health_check(request: Request):
    return ResponseSchema(
        status_code=status.HTTP_200_OK,
        message="Server đang hoạt động bình thường!",
        data={"status": "healthy"},
        errors=None,
        path=request.url.path,
    )