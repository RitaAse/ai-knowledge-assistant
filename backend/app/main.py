from fastapi import FastAPI


def create_application() -> FastAPI:
    """
    Creates and configures the FastAPI application.
    """

    application = FastAPI(
        title="AI Knowledge Assistant API",
        description="Backend API for a Retrieval-Augmented Generation application.",
        version="1.0.0",
    )

    return application


app = create_application()