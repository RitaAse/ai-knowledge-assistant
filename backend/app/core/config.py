from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration loaded from environment variables.
    """

    app_name: str = "AI Knowledge Assistant API"
    api_version: str = "1.0.0"
    environment: str = "development"

    database_url: str
    groq_api_key: str

    # Storage configuration
    storage_provider: str = "local"
    upload_directory: str = "uploads/documents"

    gcs_bucket_name: str | None = None
    gcs_project_id: str | None = None
    google_application_credentials: str | None = None

        # RAG configuration
    retrieval_top_k: int = 5
    similarity_threshold: float = 0.7


    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()