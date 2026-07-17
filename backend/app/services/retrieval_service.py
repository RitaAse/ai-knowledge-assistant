from sqlalchemy.orm import Session

from app.models.document_chunk import DocumentChunk
from app.services.embedding_service import generate_embedding


def retrieve_similar_chunks(
    question: str,
    db: Session,
    limit: int = 5,
):
    """
    Retrieve document chunks most similar
    to a user question.
    """

    question_embedding = generate_embedding(question)

    results = (
        db.query(DocumentChunk)
        .filter(
            DocumentChunk.embedding.isnot(None)
        )
        .order_by(
            DocumentChunk.embedding.cosine_distance(
                question_embedding
            )
        )
        .limit(limit)
        .all()
    )

    return results