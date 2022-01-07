from app.oauth2 import ALGORITHM, SECRET_KEY
import app.schemas as schemas
from jose import jwt
import pytest
# def test_root(client):
#     response = client.get('/')
#     assert response.json().get('message') == 'Hello fastapi learner!'
#     assert response.status_code == 200
    
def test_create_user(client):
    email = 'pepe2@test-email.com'
    password = 'pepe123'
    response = client.post('/users/', json={'email': email, 'password': password})

    new_user = schemas.UserResponse(**response.json())

    assert new_user.email == email
    assert response.status_code == 201

def test_login_user(client, test_user):
    response = client.post('/login', data={'username': test_user['email'], 'password': test_user['password']})
    login_response = schemas.Token(**response.json())
    
    payload = jwt.decode(login_response.access_token, SECRET_KEY, algorithms=[ALGORITHM])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_response.token_type == "bearer"
    assert response.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'pepe123', 403),
    ('pepe2@test-email.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'pepe123', 422),
    ('pepe2@test-email.com', None, 422)
])
def test_incorrect_login(client, email, password, status_code):
    res = client.post('/login', data={'username': email, 'password': password})
    assert res.status_code == status_code
    if status_code == 403:
        assert res.json().get('detail') == 'Invalid credentials'