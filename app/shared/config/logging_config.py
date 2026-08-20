import logging
import sys
from logging.config import dictConfig


def configure_logging(log_level: str) -> None:
    log_level = log_level.upper()

    valid_levels = {
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    }

    if log_level not in valid_levels:
        raise ValueError(f"Invalid LOG_LEVEL: {log_level}")

    dictConfig(
        {
            "version": 1,

            # Важно для логов Uvicorn, SQLAlchemy и других библиотек.
            "disable_existing_loggers": False,

            "formatters": {
                "default": {
                    "format": (
                        "%(asctime)s | "
                        "%(levelname)-8s | "
                        "%(name)s | "
                        "%(message)s"
                    ),
                },
            },

            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                    "stream": sys.stdout,
                },
            },

            "root": {
                "level": log_level,
                "handlers": ["console"],
            },

            "loggers": {
                "uvicorn": {
                    "level": log_level,
                    "handlers": ["console"],
                    "propagate": False,
                },
                "uvicorn.error": {
                    "level": log_level,
                    "handlers": [],
                    "propagate": True,
                },
                "uvicorn.access": {
                    "level": log_level,
                    "handlers": ["console"],
                    "propagate": False,
                },
            },
        }
    )