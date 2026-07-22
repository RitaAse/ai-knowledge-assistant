import structlog
import tempfile
from pathlib import Path

from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.core.status import DocumentStatus
from app.db.session import SessionLocal
from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.services.document_processor import (
    extract_pages_from_pdf,
    chunk_text,
)
from app.services.embedding_service import generate_embedding
from app.services.storage_service import get_storage

logger = structlog.get_logger()

def process_document(
    document_id: int,
):
    db: Session = SessionLocal()

    document = None

    try:
        document = (
            db.query(Document)
            .filter(Document.id == document_id)
            .first()
        )

        if document is None:
            return
        
        
        logger.info(
            "document_processing_started",
            document_id=document.id,
            filename=document.filename,
        )

        document.processing_status = DocumentStatus.PROCESSING
        document.processing_started_at = datetime.now(UTC)

        db.commit()

        logger.info(
            "document_status_updated",
            document_id=document.id,
            status="PROCESSING",
        )

        storage = get_storage()

        file_bytes = storage.get_file(
            document.file_path
        )

        if file_bytes is None:
            raise FileNotFoundError(
                "Document file could not be retrieved from storage."
            )


        with tempfile.NamedTemporaryFile(
            suffix=".pdf",
            delete=False,
        ) as temp_file:

            temp_file.write(file_bytes)
            temp_file_path = temp_file.name


        try:
            pages = extract_pages_from_pdf(
                temp_file_path
            )

        finally:
            Path(temp_file_path).unlink(
                missing_ok=True
            )

        chunks = chunk_text(
            pages
        )

        for index, chunk in enumerate(chunks):

            embedding = generate_embedding(
                chunk["content"]
            )

            db_chunk = DocumentChunk(
                document_id=document.id,
                chunk_index=index,
                page_number=chunk["page_number"],
                content=chunk["content"],
                embedding=embedding,
            )

            db.add(db_chunk)

            db.add(db_chunk)

        db.commit()

        document.processing_status = DocumentStatus.COMPLETED
        document.processing_completed_at = datetime.now(UTC)

        db.commit()

        logger.info(
            "document_processing_completed",
            document_id=document.id,
            filename=document.filename,
        )

    except Exception as error:

        logger.exception(
            "document_processing_failed",
            document_id=document_id,
        )

        if document:
            document.processing_status = DocumentStatus.FAILED
            document.error_message = str(error)

            db.commit()

    finally:
        db.close()