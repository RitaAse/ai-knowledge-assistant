from abc import ABC, abstractmethod
from pathlib import Path
from typing import BinaryIO


class BaseStorage(ABC):

    @abstractmethod
    def upload_file(
        self,
        file_bytes: bytes,
        filename: str,
    ) -> str:
        """
        Upload a file.

        Returns the storage path or blob name.
        """
        pass


    @abstractmethod
    def delete_file(
        self,
        file_path: str,
    ) -> None:
        """
        Delete a stored file.
        """
        pass


    def get_file(
        self,
        file_path: str,
    ) -> bytes | None:
        """
        Retrieve a stored file.

        Returns file contents as bytes.
        """
        pass