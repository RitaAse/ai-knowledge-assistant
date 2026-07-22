from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_upload_document(fake_storage):

    files = {
        "file": (
            "test_document.pdf",
            b"%PDF-1.4 fake pdf content",
            "application/pdf",
        )
    }

    response = client.post(
        "/documents/upload",
        files=files,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["filename"] == "test_document.pdf"

    assert data["processing_status"] == "UPLOADED"

    assert len(fake_storage.files) == 1