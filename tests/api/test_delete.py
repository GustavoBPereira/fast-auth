from fastapi.testclient import TestClient

from fast_auth.app import app

from asyncio import sleep


def test_success_delete(client, user):

    response = client.delete(f"/auth?user_id={user.id}")

    assert response.status_code == 200

    assert response.json() == {}


def test_wrong_delete(client, user):

    response = client.delete(f"/auth?user_id={user.id + 1}")

    assert response.status_code == 404

    assert response.json() == {"detail": "User not found"}
