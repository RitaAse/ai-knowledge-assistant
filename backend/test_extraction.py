from app.services.document_processor import extract_text_from_pdf


text = extract_text_from_pdf(
    "uploads/documents/9b143122-7b2c-4f57-89fd-b4c194f4c328-Sample file test.pdf"
)


print(text[:1000])