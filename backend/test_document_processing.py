from app.services.document_processor import (
    extract_text_from_pdf,
    chunk_text,
)


text = extract_text_from_pdf(
    "uploads/documents/9b143122-7b2c-4f57-89fd-b4c194f4c328-Sample file test.pdf"
)


chunks = chunk_text(
    text,
    chunk_size=800,
    overlap=150,
)

print(f"Document length: {len(text)} characters")
print(f"Number of chunks: {len(chunks)}")

for index, chunk in enumerate(chunks, start=1):
    print("=" * 60)
    print(f"Chunk {index}")
    print("=" * 60)
    print(chunk)
    print()

