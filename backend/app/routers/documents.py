from pathlib import Path
from uuid import uuid4

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    File,
    HTTPException,
    UploadFile,
)

from fastapi.responses import FileResponse

from app.services.document_processing_service import process_document

from sqlalchemy.orm import Session

from app.core.status import DocumentStatus
from app.db.dependencies import get_db
from app.models.document import Document
from app.schemas.document import DocumentCreate, DocumentResponse
from app.schemas.search import (
    SearchRequest,
    RAGResponse,
)
from app.services.rag_service import generate_answer

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)



@router.post(
    "/upload",
    response_model=DocumentResponse,
    status_code=201,
)
def upload_document(
    background_tasks: BackgroundTasks,
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

    db_document = Document(
        filename=file.filename,
        file_path=str(file_path),
        file_type=file.content_type,
        file_size=file_path.stat().st_size,
        processing_status=DocumentStatus.UPLOADED,
    )

    db.add(db_document)
    db.commit()
    db.refresh(db_document)


    background_tasks.add_task(
        process_document,
        db_document.id,
    )


    return db_document


@router.get(
    "",
    response_model=list[DocumentResponse],
)
def get_documents(
    db: Session = Depends(get_db),
):
    documents = (
        db.query(Document)
        .order_by(Document.created_at.desc())
        .all()
    )

    return documents

@router.get(
    "/{document_id}/file"
)
def get_document_file(
    document_id: int,
    db: Session = Depends(get_db),
):

    document = (
        db.query(Document)
        .filter(Document.id == document_id)
        .first()
    )

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found.",
        )


    file_path = Path(document.file_path)

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="File not found.",
        )


    return FileResponse(
        path=file_path,
        filename=document.filename,
        media_type=document.file_type,
    )

@router.get(
    "/{document_id}",
    response_model=DocumentResponse,
)
def get_document(
    document_id: int,
    db: Session = Depends(get_db),
):
    document = (
        db.query(Document)
        .filter(Document.id == document_id)
        .first()
    )

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found.",
        )

    return document

@router.delete(
    "/{document_id}",
)
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
):
    document = (
        db.query(Document)
        .filter(Document.id == document_id)
        .first()
    )

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found.",
        )

    # Delete PDF file from storage
    file_path = Path(document.file_path)

    if file_path.exists():
        file_path.unlink()

    # Delete database record
    db.delete(document)
    db.commit()

    return {
        "message": "Document deleted successfully."
    }

@router.post(
    "/search",
    response_model=RAGResponse,
)
def search_documents(
    request: SearchRequest,
    
    db: Session = Depends(get_db),
):
    answer = generate_answer(
        question=request.question,
        db=db,
    )

    return answer

