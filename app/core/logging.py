import logging
import os
import sys
import time
from contextvars import ContextVar
from logging.handlers import TimedRotatingFileHandler
from typing import Optional

# Context variable to hold per-request correlation id
request_id_ctx: ContextVar[str] = ContextVar("request_id", default="-")


class RequestIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        try:
            record.request_id = request_id_ctx.get()
        except Exception:
            record.request_id = "-"
        return True


class IsoFormatter(logging.Formatter):
    def __init__(self, fmt: Optional[str] = None, datefmt: Optional[str] = None):
        default_fmt = (
            "%(asctime)s | %(levelname)s | %(name)s | req:%(request_id)s | %(message)s"
        )
        super().__init__(fmt or default_fmt, datefmt or "%Y-%m-%dT%H:%M:%S%z")
        # Use UTC for consistency across environments
        self.converter = time.gmtime


_initialized = False


def _build_handler(handler: logging.Handler, level: int, formatter: logging.Formatter, add_filter: logging.Filter) -> logging.Handler:
    handler.setLevel(level)
    handler.setFormatter(formatter)
    handler.addFilter(add_filter)
    return handler


def init_logging(env: str = "development", log_dir: Optional[str] = None, base_level: Optional[int] = None) -> None:
    global _initialized
    if _initialized:
        return

    # Determine base level
    env = (env or "").lower()
    base_level = base_level if base_level is not None else (logging.DEBUG if env in {"dev", "development", "local"} else logging.INFO)

    # Ensure log directory exists
    log_dir = log_dir or os.path.join(os.getcwd(), "logs")
    os.makedirs(log_dir, exist_ok=True)

    # Formatters and filters
    formatter = IsoFormatter()
    req_filter = RequestIdFilter()

    # Handlers
    console_handler = _build_handler(logging.StreamHandler(stream=sys.stdout), base_level, formatter, req_filter)

    app_file_path = os.path.join(log_dir, "app.log")
    app_file_handler = _build_handler(
        TimedRotatingFileHandler(app_file_path, when="midnight", backupCount=7, encoding="utf-8"),
        logging.INFO,
        formatter,
        req_filter,
    )

    error_file_path = os.path.join(log_dir, "error.log")
    error_file_handler = _build_handler(
        TimedRotatingFileHandler(error_file_path, when="midnight", backupCount=14, encoding="utf-8"),
        logging.ERROR,
        formatter,
        req_filter,
    )

    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(base_level)

    # Avoid duplicate handlers if uvicorn reload spawns processes
    root_logger.handlers.clear()
    root_logger.addHandler(console_handler)
    root_logger.addHandler(app_file_handler)
    root_logger.addHandler(error_file_handler)

    # Align common third-party loggers
    for name in ("uvicorn", "uvicorn.error", "uvicorn.access", "sqlalchemy"):
        lg = logging.getLogger(name)
        lg.setLevel(logging.INFO if name.startswith("uvicorn") else base_level)
        lg.handlers.clear()
        lg.addHandler(console_handler)
        lg.addHandler(app_file_handler)
        lg.addHandler(error_file_handler)
        lg.propagate = False

    _initialized = True


def get_logger(name: Optional[str] = None) -> logging.Logger:
    return logging.getLogger(name or __name__)


def set_request_id(req_id: str) -> None:
    request_id_ctx.set(req_id)


def reset_request_id() -> None:
    request_id_ctx.set("-")
