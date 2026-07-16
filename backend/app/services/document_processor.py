import fitz
from langchain_text_splitters import RecursiveCharacterTextSplitter


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

def chunk_text(
    text: str,
    chunk_size: int = 1000,
    overlap: int = 200,
) -> list[str]:
    """
    Split text using LangChain RecursiveCharacterTextSplitter.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
    )

    chunks = text_splitter.split_text(text)

    return chunks