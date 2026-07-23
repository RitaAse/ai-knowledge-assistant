from google.cloud import storage

from app.core.config import settings
from app.services.storage.base import BaseStorage


class GCSStorage(BaseStorage):

    def __init__(self):

        if not settings.gcs_bucket_name:
            raise ValueError(
                "GCS bucket name is not configured."
            )

        self.client = storage.Client(
            project=settings.gcs_project_id
        )

        self.bucket = self.client.bucket(
            settings.gcs_bucket_name
        )


    def upload_file(
        self,
        file_bytes: bytes,
        filename: str,
    ) -> str:

        blob = self.bucket.blob(
            f"documents/{filename}"
        )

        blob.upload_from_string(
            file_bytes
        )

        return blob.name


    def delete_file(
        self,
        file_path: str,
    ) -> None:

        blob = self.bucket.blob(
            file_path
        )

        blob.delete()


    def get_file(
        self,
        file_path: str,
    ) -> bytes | None:

        blob = self.bucket.blob(
            file_path
        )

        if not blob.exists():
            return None

        return blob.download_as_bytes()


    def health_check(self) -> bool:
        try:
            self.bucket.reload()
            return True

        except Exception:
            return False