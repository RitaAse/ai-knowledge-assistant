from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.core.status import DocumentStatus
from app.db.session import SessionLocal
from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.services.document_processor import (
    extract_text_from_pdf,
    chunk_text,
)
from app.services.embedding_service import generate_embedding


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
        print("STARTING DOCUMENT PROCESSING")

        document.processing_status = DocumentStatus.PROCESSING
        document.processing_started_at = datetime.now(UTC)

        db.commit()

        print("STATUS CHANGED TO PROCESSING")

        text = extract_text_from_pdf(
            document.file_path
        )

        chunks = chunk_text(text)

        for index, chunk in enumerate(chunks):

            embedding = generate_embedding(chunk)

            db_chunk = DocumentChunk(
                document_id=document.id,
                chunk_index=index,
                content=chunk,
                embedding=embedding,
            )

            db.add(db_chunk)

        db.commit()

        document.processing_status = DocumentStatus.COMPLETED
        document.processing_completed_at = datetime.now(UTC)

        db.commit()

        print("DOCUMENT PROCESSING COMPLETED")

    except Exception as error:

        print(error)

        if document:
            document.processing_status = DocumentStatus.FAILED
            document.error_message = str(error)
            
            db.commit()

    finally:
        db.close()