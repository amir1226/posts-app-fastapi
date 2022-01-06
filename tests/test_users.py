from fastapi.testclient import TestClient
from app.main import app
import app.schemas as schemas

client = TestClient(app)

def test_root():
    response = client.get('/')
    assert response.json().get('message') == 'Hello fastapi learner!'
    assert response.status_code == 200

def test_create_user():
    email = 'pepe2@test-email.com'
    password = 'pepe123'
    response = client.post('/users/', json={'email': email, 'password': password})

    new_user = schemas.UserResponse(**response.json())

    assert new_user.email == email
    assert response.status_code == 201