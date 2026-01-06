from __future__ import annotations

from pathlib import Path
from dotenv import load_dotenv

from app.core.config import AppConfig, load_config
from app.core.paths import ensure_dir
from app.core.logger import setup_loguru, logger


def boot(log_name: str) -> AppConfig:
    load_dotenv(override=True)

    config = load_config()

    log_dir = ensure_dir(config.root / "logs")
    log_file = log_dir / f"{log_name}.log"

    setup_loguru(level=config.log_level, log_file=log_file)
    logger.info("System initialized.")
    logger.debug(f"AppConfig: {config.model_dump()}")

    return config
