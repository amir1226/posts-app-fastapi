import app.schemas as schemas
from .database import client, session

def test_root(client):
    response = client.get('/')
    assert response.json().get('message') == 'Hello fastapi learner!'
    assert response.status_code == 200

def test_create_user(client):
    email = 'pepe2@test-email.com'
    password = 'pepe123'
    response = client.post('/users/', json={'email': email, 'password': password})

    new_user = schemas.UserResponse(**response.json())

    assert new_user.email == email
    assert response.status_code == 201

