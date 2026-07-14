from fastapi import APIRouter, Depends
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