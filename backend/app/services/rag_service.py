import structlog
logger = structlog.get_logger()

from sqlalchemy.orm import Session

from app.core.config import settings
from app.services.llm_service import get_llm
from app.services.retrieval_service import retrieve_similar_chunks


def generate_answer(
    question: str,
    db: Session,
) -> dict:

    results = retrieve_similar_chunks(
        question=question,
        db=db,
        limit=settings.retrieval_top_k,
        include_distance=True,
    )

    for row in results:
        logger.info(
            "retrieved_chunk",
            document=getattr(
                row.DocumentChunk.document,
                "filename",
                None,
            ),
            page=row.DocumentChunk.page_number,
            chunk=row.DocumentChunk.chunk_index,
            distance=float(row.distance),
            preview=row.DocumentChunk.content[:120],
        )

    results = [
        row
        for row in results
        if row.distance <= settings.similarity_threshold
    ]


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

Strict rules:
1. Use only information explicitly present in the context.
2. Do not assume the document refers to a company, person, or organization unless it is explicitly mentioned.
3. If the user asks about a specific entity that is not mentioned in the context, clearly state that it was not found.
4. You may provide related information from the context only if you clearly state that it is general information and not about the missing entity.
5. Never invent missing details.

If the answer cannot be found, say:
"I could not find that information in the uploaded documents."

Do not provide related information unless it directly answers the question.

Context:
{context}

Question:
{question}

Answer:
"""

    llm = get_llm()

    try:
        response = llm.invoke(prompt)
        answer_text = response.content

    except Exception:

        logger.exception(
            "llm_generation_failed"
        )

        return {
            "answer": "I was unable to generate an answer at this time.",
            "sources": [],
        }

    sources = []

    seen_documents = set()

    for row in results:

        document_name = (
            row.DocumentChunk.document.filename
        )

        if document_name not in seen_documents:

            sources.append(
                {
                    "document": document_name,
                    "page": row.DocumentChunk.page_number,
                    "relevance": calculate_relevance(
                        float(row.distance)
                    ),
                    "preview": row.DocumentChunk.content[:300],
                }
            )

            seen_documents.add(document_name)


        if len(sources) == 3:
            break


    if answer_text.startswith(
        "I could not find that information"
    ):
        sources = []


    return {
        "answer": answer_text,
        "sources": sources,
    }

    
def calculate_relevance(distance: float) -> int:
    relevance = (1 - distance) * 100
    return round(relevance)