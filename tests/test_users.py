from app.oauth2 import ALGORITHM, SECRET_KEY
import app.schemas as schemas
from jose import jwt

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
