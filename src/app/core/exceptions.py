from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from loguru import logger

def setup_exception_handlers(app: FastAPI):
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        logger.warning(f"HTTP Exception {exc.status_code} на {request.url}: {exc.detail}")
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.error(f"Ошибка валидации на {request.url}: {exc.errors()}")
        return JSONResponse(
            status_code=422,
            content={"detail": "Ошибка валидации данных", "errors": exc.errors()}
        )

    @app.exception_handler(Exception)
    async def exception_handler(request: Request, exc: Exception):
        logger.exception(f"Критическая ошибка на {request.url}: {exc}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Внутренняя ошибка сервера"}
        )