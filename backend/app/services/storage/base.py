from abc import ABC, abstractmethod


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


    @abstractmethod
    def get_file(
        self,
        file_path: str,
    ):
        """
        Retrieve a stored file.
        """
        pass