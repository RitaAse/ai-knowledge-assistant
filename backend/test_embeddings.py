from app.services.embedding_service import generate_embedding


embedding = generate_embedding(
    "Employees should use strong passwords."
)

print(f"Embedding length: {len(embedding)}")
print()

print(embedding[:10])