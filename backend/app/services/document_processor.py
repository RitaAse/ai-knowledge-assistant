import fitz

from langchain_text_splitters import RecursiveCharacterTextSplitter


def extract_pages_from_pdf(
    file_path: str,
) -> list[dict]:
    """
    Extract text from PDF while preserving page numbers.
    """

    document = fitz.open(file_path)

    pages = []

    for page_number, page in enumerate(document, start=1):

        text = page.get_text()

        if text.strip():

            pages.append(
                {
                    "page_number": page_number,
                    "text": text,
                }
            )

    document.close()

    return pages



def chunk_text(
    pages: list[dict],
    chunk_size: int = 1000,
    overlap: int = 200,
) -> list[dict]:
    """
    Split PDF text into chunks while preserving page metadata.
    """

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            "",
        ],
    )

    chunks = []

    for page in pages:

        page_chunks = text_splitter.split_text(
            page["text"]
        )

        for chunk in page_chunks:

            chunks.append(
                {
                    "content": chunk,
                    "page_number": page["page_number"],
                }
            )

    return chunks