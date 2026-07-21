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

    storage_provider: str = "local"

    gcs_bucket_name: str | None = None
    gcs_project_id: str | None = None


    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()