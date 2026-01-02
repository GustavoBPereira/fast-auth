from fastapi.testclient import TestClient

from fast_auth.app import app


def test_success_get(client, user):

    response = client.get("/auth")

    assert response.status_code == 200

    assert response.json() == {
        "users": [
            {
                "id": user.id,
                "username": user.username,
                "created_at": user.created_at.isoformat()
            }
        ]
    }

