from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_rag_search():

    response = client.post(
        "/documents/search",
        json={
            "question": "What operating system is recommended?"
        },
    )


    assert response.status_code == 200


    data = response.json()


    assert "answer" in data

    assert "sources" in data

    assert isinstance(
        data["sources"],
        list,
    )