from datetime import datetime

from pydantic import BaseModel


class DocumentCreate(BaseModel):
    filename: str


class DocumentResponse(BaseModel):
    id: int
    filename: str
    file_path: str
    file_type: str
    file_size: int
    processing_status: str
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }