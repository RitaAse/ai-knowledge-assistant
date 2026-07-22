from app.services.storage.base import BaseStorage


class FakeStorage(BaseStorage):

    def __init__(self):
        self.files = {}

    def upload_file(
        self,
        file_bytes: bytes,
        filename: str,
    ) -> str:

        self.files[filename] = file_bytes

        return filename


    def get_file(
        self,
        file_path: str,
    ) -> bytes | None:

        return self.files.get(file_path)


    def delete_file(
        self,
        file_path: str,
    ) -> None:

        if file_path in self.files:
            del self.files[file_path]