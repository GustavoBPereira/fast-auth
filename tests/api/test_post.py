from fastapi.testclient import TestClient
from sqlalchemy import select

from fast_auth.app import app
from fast_auth.models import User


def test_success_post(client, mock_db_time):

    with mock_db_time(model=User):
        response = client.post("/auth", json={
                'username': 'Luyi',
                'password': 'secret',
        })

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "username": "Luyi",
        "created_at": "2024-01-01T00:00:00"
    }


