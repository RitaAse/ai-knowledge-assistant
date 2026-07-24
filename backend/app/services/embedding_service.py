from sentence_transformers import SentenceTransformer


_embedding_model = None


def get_embedding_model() -> SentenceTransformer:
    """
    Lazy-load the embedding model only when needed.
    This prevents loading the model during application startup.
    """

    global _embedding_model

    if _embedding_model is None:
        _embedding_model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

    return _embedding_model


def generate_embedding(
    text: str,
) -> list[float]:
    """
    Generate an embedding for a piece of text.
    """

    embedding_model = get_embedding_model()

    embedding = embedding_model.encode(
        text,
        convert_to_numpy=True,
    )

    return embedding.tolist()