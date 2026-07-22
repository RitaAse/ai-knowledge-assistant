from app.core.config import settings 



from app.services.storage.base import BaseStorage

from app.services.storage.local_storage import LocalStorage





def get_storage() -> BaseStorage:

    """

    Returns the configured storage provider.

    """



    if settings.storage_provider == "local":



        return LocalStorage()



    elif settings.storage_provider == "gcs":



        from app.services.storage.gcs_storage import GCSStorage



        return GCSStorage()



    else:

        raise ValueError(

            f"Unsupported storage provider: {settings.storage_provider}"

        )