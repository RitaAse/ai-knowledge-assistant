from fastapi import FastAPI

from app.core.config import settings


def create_application() -> FastAPI:
    application = FastAPI(
        title=settings.app_name,
        version=settings.api_version,
        description="Backend API for a Retrieval-Augmented Generation application.",
    )

    return application


app = create_application()