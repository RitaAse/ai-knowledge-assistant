import structlog
from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import AppException

 
logger = structlog.get_logger()


async def app_exception_handler(
    request: Request,
    exc: AppException,
) -> JSONResponse:
    """
    Handles application-specific exceptions.
    """

    logger.error(
        "application_error",
        request_id=request.state.request_id,
        code=exc.code,
        message=exc.message,
        path=request.url.path,
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "request_id": request.state.request_id,
            }
        },
    )