from sqlalchemy.orm import Session

from app.models.document_chunk import DocumentChunk
from app.services.embedding_service import generate_embedding

from app.core.config import settings


def retrieve_similar_chunks(
    question: str,
    db: Session,
    limit: int = 8,
    include_distance: bool = False,
):
    """
    Retrieve document chunks most similar
    to a user question.

    Uses cosine distance:
    - Lower distance = more similar
    - Higher distance = less similar
    """

    question_embedding = generate_embedding(question)

    distance = DocumentChunk.embedding.cosine_distance(
        question_embedding
    ).label("distance")

    query = (
        db.query(
            DocumentChunk,
            distance,
        )
        .filter(
            DocumentChunk.embedding.isnot(None)
        )
        .order_by(distance)
        .limit(limit)
    )

    results = query.all()

    # Remove weak matches
    filtered_results = [
        row
        for row in results
        if row.distance <= settings.similarity_threshold
    ]

    if include_distance:
        return filtered_results

    return [
        row.DocumentChunk
        for row in filtered_results
    ]