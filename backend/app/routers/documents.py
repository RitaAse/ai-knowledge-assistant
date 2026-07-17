from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.core.status import DocumentStatus
from app.db.dependencies import get_db
from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.schemas.document import DocumentCreate, DocumentResponse
from app.schemas.search import SearchRequest
from app.services.document_processor import (
    extract_text_from_pdf,
    chunk_text,
)

from app.services.embedding_service import generate_embedding

from app.services.retrieval_service import retrieve_similar_chunks

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

    db_document.processing_status = DocumentStatus.PROCESSING

    db.commit()
    db.refresh(db_document)

    try:
        text = extract_text_from_pdf(
            db_document.file_path
        )

        chunks = chunk_text(text)

        for index, chunk in enumerate(chunks):
            embedding = generate_embedding(chunk)

            db_chunk = DocumentChunk(
                document_id=db_document.id,
                chunk_index=index,
                content=chunk,
                embedding=embedding,
            )

            db.add(db_chunk)

        db.commit()

        db_document.processing_status = DocumentStatus.COMPLETED

        db.commit()
        db.refresh(db_document)

    except Exception as error:
        print(error)
        db_document.processing_status = DocumentStatus.FAILED

        db.commit()
        db.refresh(db_document)


    return db_document

@router.post("/search")
def search_documents(
    request: SearchRequest,
    db: Session = Depends(get_db),
):
    results = retrieve_similar_chunks(
        question=request.question,
        db=db,
        limit=5,
    )

    return {
        "results": [
            {
                "chunk_index": chunk.chunk_index,
                "distance": distance,
                "content": chunk.content,
            }
            for chunk, distance in results
        ]
    }