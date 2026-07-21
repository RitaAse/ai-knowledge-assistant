from fastapi import FastAPI

from app.routers.documents import router as documents_router
from app.routers.health import router as health_router

from app.core.config import settings
from app.core.logging import configure_logging
from app.core.exception_handlers import app_exception_handler
from app.core.exceptions import AppException
from app.middleware.logging import LoggingMiddleware



def create_application() -> FastAPI:
    configure_logging()

    application = FastAPI(
        title=settings.app_name,
        version=settings.api_version,
        description="Backend API for a Retrieval-Augmented Generation application.",
    )

    application.add_middleware(LoggingMiddleware)

    application.add_exception_handler(
        AppException,
        app_exception_handler,
    )

    application.include_router(documents_router)
    application.include_router(health_router)

    return application


app = create_application()