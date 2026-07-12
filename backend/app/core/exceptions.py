from typing import Any


class AppException(Exception):
    """
    Base exception for application-specific errors.
    """

    def __init__(
        self,
        message: str,
        code: str,
        status_code: int,
        details: dict[str, Any] | None = None,
    ):
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details

        super().__init__(message)

class AuthenticationError(AppException):
    """
    Raised when authentication fails.
    """

    def __init__(
        self,
        message: str = "Authentication failed",
        details: dict | None = None,
    ):
        super().__init__(
            message=message,
            code="AUTHENTICATION_FAILED",
            status_code=401,
            details=details,
        )


class DocumentProcessingError(AppException):
    """
    Raised when document ingestion or processing fails.
    """

    def __init__(
        self,
        message: str = "Document processing failed",
        details: dict | None = None,
    ):
        super().__init__(
            message=message,
            code="DOCUMENT_PROCESSING_FAILED",
            status_code=400,
            details=details,
        )


class VectorDatabaseError(AppException):
    """
    Raised when vector database operations fail.
    """

    def __init__(
        self,
        message: str = "Vector database operation failed",
        details: dict | None = None,
    ):
        super().__init__(
            message=message,
            code="VECTOR_DATABASE_ERROR",
            status_code=503,
            details=details,
        )


class LLMProviderError(AppException):
    """
    Raised when the language model provider fails.
    """

    def __init__(
        self,
        message: str = "Language model service unavailable",
        details: dict | None = None,
    ):
        super().__init__(
            message=message,
            code="LLM_PROVIDER_ERROR",
            status_code=502,
            details=details,
        )