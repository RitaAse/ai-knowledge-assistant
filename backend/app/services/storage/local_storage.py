from pathlib import Path

from app.services.storage.base import BaseStorage
from app.core.config import settings

class LocalStorage(BaseStorage):

    def __init__(
        self,
        upload_directory: str = settings.upload_directory,
    ):
        self.upload_directory = Path(upload_directory)

        self.upload_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    def upload_file(
        self,
        file_bytes: bytes,
        filename: str,
    ) -> str:

        file_path = self.upload_directory / filename

        with file_path.open("wb") as buffer:
            buffer.write(file_bytes)

        return str(file_path)

    def delete_file(
        self,
        file_path: str,
    ) -> None:

        path = Path(file_path)

        if path.exists():
            path.unlink()

    def get_file(
        self,
        file_path: str,
    ) -> bytes | None:

        path = Path(file_path)

        if not path.exists():
            return None

        return path.read_bytes()
    
    def health_check(self) -> bool:
        return self.upload_directory.exists()