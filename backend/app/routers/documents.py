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
from app.schemas.document import DocumentResponse
from app.schemas.search import (
    SearchRequest,
    RAGResponse,
)
from app.services.rag_service import generate_answer
from app.services.storage_service import get_storage
from app.services.storage.base import BaseStorage

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)



@router.post(
    "/upload",
    response_model=DocumentResponse,
    status_code=201,
    summary="Upload a document",
    description=(
        "Uploads a PDF document to the configured storage provider "
        "and starts asynchronous document processing."
    ),
    responses={
        201: {
            "description": "Document uploaded successfully."
        },
        400: {
            "description": "Invalid document or processing failed."
        },
        500: {
            "description": "Unexpected server error."
        },
    },
)

def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    storage: BaseStorage = Depends(get_storage),
):
    

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
    summary="List uploaded documents",
    description=(
        "Returns all uploaded documents ordered by creation date, "
        "with their current processing status."
    ),
    responses={
        200: {
            "description": "Documents retrieved successfully."
        },
        500: {
            "description": "Unexpected server error."
        },
    },
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
    "/{document_id}/file",
    summary="Download original document",
    description=(
        "Retrieves the uploaded document file from storage."
    ),
    responses={
        200: {
            "description": "File retrieved successfully."
        },
        404: {
            "description": "Document or file not found."
        },
        500: {
            "description": "Unexpected server error."
        },
    },
)

def get_document_file(
    document_id: int,
    db: Session = Depends(get_db),
    storage: BaseStorage = Depends(get_storage),
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
    summary="Retrieve document details",
    description=(
        "Returns metadata and processing status for a specific document."
    ),
    responses={
        200: {
            "description": "Document retrieved successfully."
        },
        404: {
            "description": "Document not found."
        },
        500: {
            "description": "Unexpected server error."
        },
    },
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
    summary="Delete a document",
    description=(
        "Deletes a document record and removes the associated file "
        "from the configured storage provider."
    ),
    responses={
        200: {
            "description": "Document deleted successfully."
        },
        404: {
            "description": "Document not found."
        },
        500: {
            "description": "Unexpected server error."
        },
    },
)

def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    storage: BaseStorage = Depends(get_storage),
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

