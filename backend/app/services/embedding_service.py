from sentence_transformers import SentenceTransformer


embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)


def generate_embedding(
    text: str,
) -> list[float]:
    """
    Generate an embedding for a piece of text.
    """

    embedding = embedding_model.encode(
        text,
        convert_to_numpy=True,
    )

    return embedding.tolist()