from fastapi.testclient import TestClient
from main import app
from api_helper import ApiHelper
from models import User
from unittest.mock import patch

client = TestClient(app)

@patch.object(ApiHelper, 'get_users', return_value={"users": [], "last_evaluated_key": None})
def test_get_users(mock_get_users):
    response = client.get("/users")
    assert response.status_code == 200
    assert "users" in response.json()

@patch.object(ApiHelper, 'add_user', return_value={"uuid": "123", "name": "John", "surname": "Doe", "email": "john.doe@example.com"})
def test_add_user(mock_add_user):
    new_user = {"name": "John", "surname": "Doe", "email": "john.doe@example.com"}
    response = client.post("/users", json=new_user)
    assert response.status_code == 200
    assert response.json()["name"] == "John"
    assert response.json()["surname"] == "Doe"
