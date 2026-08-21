from app.db.database import Base, engine
from app.schemas.response import ErrorResponseSchema, ResponseSchema
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Event Management API")

@app.get("/health", response_model=ResponseSchema, tags=["Health"])
def health_check(request: Request):
    return ResponseSchema(
        status_code=status.HTTP_200_OK,
        message="Server đang hoạt động bình thường!",
        data={"status": "healthy"},
        errors=None,
        path=request.url.path,
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponseSchema(
            status_code=exc.status_code,
            message=str(exc.detail),
            data=None,
            errors=None,
            path=request.url.path,
        ).model_dump(mode="json"),
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ErrorResponseSchema(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            message="Dữ liệu đầu vào không hợp lệ",
            data=None,
            errors=exc.errors(),
            path=request.url.path,
        ).model_dump(mode="json"),
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponseSchema(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Đã xảy ra lỗi hệ thống, vui lòng thử lại sau!",
            data=None,
            errors=str(exc),
            path=request.url.path,
        ).model_dump(mode="json"),
    )