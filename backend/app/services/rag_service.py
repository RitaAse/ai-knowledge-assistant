from sqlalchemy.orm import Session

from app.services.llm_service import get_llm
from app.services.retrieval_service import retrieve_similar_chunks


def generate_answer(
    question: str,
    db: Session,
) -> dict:

    results = retrieve_similar_chunks(
        question=question,
        db=db,
        limit=5,
        include_distance=True,
    )

    if not results:
        return {
            "answer": "I could not find any relevant information in the uploaded documents.",
            "sources": [],
        }

    chunks = [
        row.DocumentChunk
        for row in results
    ]

    context = "\n\n".join(
        chunk.content
        for chunk in chunks
    )

    prompt = f"""
You are an AI assistant that answers questions using only the provided context.

If the answer cannot be found in the context, say:
"I could not find that information in the uploaded documents."

Context:
{context}

Question:
{question}

Answer:
"""

    llm = get_llm()

    response = llm.invoke(prompt)

    sources = [
        {
            "document": row.DocumentChunk.document.filename,
            "chunk_index": row.DocumentChunk.chunk_index,
            "distance": float(row.distance),
            "preview": row.DocumentChunk.content[:200],
        }
        for row in results
    ]
    
    return {
        "answer": response.content,
        "sources": sources,
    }