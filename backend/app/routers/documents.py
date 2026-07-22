from uuid import uuid4

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    File,
    HTTPException,
    UploadFile,
)

from fastapi.responses import Response

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
from app.services.storage_service import get_storage

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
    storage = get_storage()

    unique_filename = f"{uuid4()}-{file.filename}"

    file_bytes = file.file.read()

    file_path = storage.upload_file(
        file_bytes=file_bytes,
        filename=unique_filename,
    )

    db_document = Document(
        filename=file.filename,
        file_path=file_path,
        file_type=file.content_type,
        file_size=len(file_bytes),
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


    storage = get_storage()

    file_bytes = storage.get_file(
        document.file_path
    )

    if file_bytes is None:
        raise HTTPException(
            status_code=404,
            detail="File not found.",
        )


    return Response(
        content=file_bytes,
        media_type=document.file_type,
        headers={
            "Content-Disposition": (
                f'attachment; filename="{document.filename}"'
            )
        },
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
    storage = get_storage()

    storage.delete_file(
        document.file_path
    )

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

