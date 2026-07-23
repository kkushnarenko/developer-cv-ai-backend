from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from src.app.api.v1.routers import api_router
from src.app.core.config import config
from src.app.core.exceptions import setup_exception_handlers
from src.app.core.limiter import setup_limiter
from fastapi.responses import RedirectResponse

# Логирование
logger.add(
    "logs/app.log",
    rotation="10 MB",
    retention="10 days",
    level="INFO",
    encoding="utf-8"
)

# Используем lifespan вместо on_event
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Сервис успешно запущен!")
    yield
    logger.info("Сервис остановлен.")


app = FastAPI(
    title=config.APP_NAME,
    description="Backend API для формы обратной связи с ИИ-анализом обращений",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Лимитер и ошибки
setup_limiter(app)
setup_exception_handlers(app)

# Подключение роутера
app.include_router(api_router)

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=config.PORT, reload=config.DEBUG)