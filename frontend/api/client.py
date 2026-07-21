import requests

from config import API_URL


def upload_document(file):
    """
    Upload a document to the FastAPI backend.
    """

    response = requests.post(
        f"{API_URL}/documents/upload",
        files={
            "file": (
                file.name,
                file,
                file.type,
            )
        },
    )

    response.raise_for_status()

    return response.json()


def get_documents():
    """
    Retrieve uploaded documents.
    """

    response = requests.get(
        f"{API_URL}/documents"
    )

    response.raise_for_status()

    return response.json()


def ask_question(question: str):
    """
    Send a question to the RAG endpoint.
    """

    response = requests.post(
        f"{API_URL}/documents/search",
        json={
            "question": question,
        },
    )

    response.raise_for_status()

    return response.json()

def delete_document(document_id: int):
    """
    Delete a document from the backend.
    """

    response = requests.delete(
        f"{API_URL}/documents/{document_id}"
    )

    response.raise_for_status()

    return response.json()

def get_document(document_id: int):
    """
    Retrieve a single document and its status.
    """

    response = requests.get(
        f"{API_URL}/documents/{document_id}"
    )

    if response.status_code == 404:
        return None

    response.raise_for_status()

    return response.json()

def search_documents(question: str):

    response = requests.post(
        f"{API_URL}/documents/search",
        json={
            "question": question,
        },
    )

    response.raise_for_status()

    return response.json()