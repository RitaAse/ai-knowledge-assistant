from sqlalchemy.orm import Session

from app.models.document_chunk import DocumentChunk
from app.services.embedding_service import generate_embedding


def retrieve_similar_chunks(
    question: str,
    db: Session,
    limit: int = 5,
    include_distance: bool = False,
    distance_threshold: float = 0.50,
):
    """
    Retrieve document chunks most similar
    to a user question.

    Uses cosine distance:
    - Lower distance = more similar
    - Higher distance = less similar
    """

    question_embedding = generate_embedding(question)

    distance = DocumentChunk.embgitedding.cosine_distance(
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
        if row.distance <= distance_threshold
    ]

    if include_distance:
        return filtered_results

    return [
        row.DocumentChunk
        for row in filtered_results
    ]