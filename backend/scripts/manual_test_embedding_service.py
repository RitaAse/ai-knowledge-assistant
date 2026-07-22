from app.services.embedding_service import generate_embedding


text = "Employees receive annual paid leave."


embedding = generate_embedding(text)


print("Embedding length:", len(embedding))
print("First 5 values:", embedding[:5])