import logging.config
import os

def setup_logging():
    os.makedirs("logs", exist_ok=True)

    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "level": "INFO",
            },
            "file_error": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "default",
                "filename": "logs/error.log",
                "maxBytes": 1024 * 1024 * 5,
                "backupCount": 3,
                "encoding": "utf8",
                "level": "ERROR",
            },
        },
        "loggers": {
            "custom_log": {
                "level": "INFO",
                "handlers": ["console", "file_error"],
                "propagate": False
            },
        },
    }

    logging.config.dictConfig(config)
