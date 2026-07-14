import fitz


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text content from a PDF file.

    Args:
        file_path: Location of the PDF file.

    Returns:
        Extracted text from the document.
    """

    document = fitz.open(file_path)

    extracted_text = []

    for page in document:
        text = page.get_text()

        extracted_text.append(text)

    document.close()

    return "\n".join(extracted_text)