import logging
from logging.config import dictConfig
from functools import lru_cache
from tds.calculator.common.configuration import config

log_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(asctime)s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",

        },
        "detailed": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(asctime)s %(name)s %(funcName)s L%(lineno)-4d %(message)s   call_trace=%(pathname)s L%(lineno)-4d",
            "datefmt": "%Y-%m-%d %H:%M:%S",

        }
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "file_handler": {
            "formatter": "detailed",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": config.LOG_FILE,
            "maxBytes": 1024 * 1024,
            "backupCount": 5

        },
    },
    "loggers": {
        "default-logger": {"handlers": ["default"], "level": "DEBUG"},
    },
}


@lru_cache()
def get_logger(class_name, log_level="DEBUG"):
    log_config["loggers"][class_name] = {"handlers": ["file_handler"], "level": log_level}
    dictConfig(log_config)
    logger = logging.getLogger(class_name)
    return logger
