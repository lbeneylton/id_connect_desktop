# app/core/logger.py

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


class LoggerConfig:
    def __init__(
        self,
        log_name: str = "app",
        log_file: str = "app.log",
        log_dir: str = "logs",
        level=logging.DEBUG,
    ):
        self.log_name = log_name
        self.log_file = log_file
        self.log_dir = Path(log_dir)
        self.level = level

        self.logger = self._setup_logger()

    def _setup_logger(self, console:bool = False) -> logging.Logger:
        self.log_dir.mkdir(exist_ok=True)

        # Formatos de log e data
        log_format = (
            "[%(asctime)s] %(levelname)s %(name)s - %(message)s"
        )
        date_format = "%d-%m-%Y %H:%M:%S"

        formatter = logging.Formatter(log_format, datefmt=date_format)

        file_handler = RotatingFileHandler(
            self.log_dir / self.log_file,
            maxBytes=5 * 1024 * 1024,
            backupCount=3,
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)

        if console:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)

        logger = logging.getLogger(self.log_name)
        logger.setLevel(self.level)

        # evita duplicar handlers
        if not logger.handlers:
            logger.addHandler(file_handler)
            if console:
                logger.addHandler(console_handler)

        logger.propagate = False

        return logger

    def get_logger(self) -> logging.Logger:
        return self.logger
    
    
logger = LoggerConfig(
    log_name="app",
).get_logger()