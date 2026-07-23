from typing import Optional
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE_PATH = BASE_DIR / ".env"

class Config(BaseSettings):
    APP_NAME: str = "Developer CV API"
    DEBUG: bool = True
    PORT: int = 8000

    GIGACHAT_CREDENTIALS: Optional[str] = None
    GIGACHAT_SCOPE: str = "GIGACHAT_API_PERS"

    MAIL_USERNAME: str = ""
    MAIL_PASSWORD: str = ""
    MAIL_FROM: str = ""
    MAIL_PORT: int = 465
    MAIL_SERVER: str = "smtp.yandex.ru"
    MAIL_FROM_NAME: str = "Developer CV Site"
    ADMIN_EMAIL: str = ""

    # Настройки автоматической загрузки из .env файла
    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        env_file_encoding="utf-8",
        extra="ignore"  # Игнорировать лишние переменные из .env
    )

config = Config()