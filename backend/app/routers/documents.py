from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models.document import Document
from app.schemas.document import DocumentCreate, DocumentResponse

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.post(
    "",
    response_model=DocumentResponse,
    status_code=201,
)
def create_document(
    document: DocumentCreate,
    db: Session = Depends(get_db),
):
    db_document = Document(
        filename=document.filename,
    )

    db.add(db_document)
    db.commit()
    db.refresh(db_document)

    return db_document

@router.post(
    "/upload",
    response_model=DocumentResponse,
    status_code=201,
)
def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    upload_directory = Path("uploads/documents")

    upload_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    unique_filename = f"{uuid4()}-{file.filename}"

    file_path = upload_directory / unique_filename

    with file_path.open("wb") as buffer:
        buffer.write(file.file.read())

    document = Document(
        filename=file.filename,
        file_path=str(file_path),
        file_type=file.content_type,
        file_size=file_path.stat().st_size,
        processing_status="UPLOADED",
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document