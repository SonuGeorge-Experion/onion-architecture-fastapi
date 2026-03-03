from fastapi import FastAPI

from app.api import routes
from app.api.exceptions.error_handler import register_exception_handlers
from app.api.middleware.request_id import RequestIdMiddleware
from app.core.config import settings
from app.core.logging import get_logger, init_logging

# Initialize logging before app creation to catch early logs
init_logging(env=settings.ENVIRONMENT)
logger = get_logger(__name__)

app = FastAPI()

# Register middleware for request correlation
app.add_middleware(RequestIdMiddleware)

# Routers
app.include_router(routes.router, prefix="/api")

# Register exception handlers
register_exception_handlers(app)

logger.info("Application startup complete")
