from fastapi.testclient import TestClient
from app.database import get_db
import pytest
from app.main import app
import app.schemas as schemas
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_user}:{settings.database_psw}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        
app.dependency_overrides[get_db] = override_get_db
        


@pytest.fixture
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    return TestClient(app)

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

