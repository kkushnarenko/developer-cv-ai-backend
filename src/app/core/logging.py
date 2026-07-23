import sys
from pathlib import Path
from loguru import logger

LOG_DIR = Path("storage/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "app.log"

def setup_logger():
    logger.remove()
    logger.add(
        sys.stdout,
        format="{time} {level} {message}",
        level="INFO"
    )
    logger.add(
        LOG_FILE,
        level="DEBUG",
        rotation="5 MB",
        retention="10 days",
        compression="zip",
        encoding="utf-8",
    )
    return logger