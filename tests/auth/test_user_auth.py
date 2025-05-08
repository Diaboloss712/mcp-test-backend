import pytest
from unittest.mock import AsyncMock, patch
from sqlmodel import Session, select
from app.models.user import User
from app.schemas.user import UserSocialCreate
from app.services.user_service import get_user_from_social_or_fail, create_user_from_social_info
from fastapi.testclient import TestClient
from app.main import app
from pydantic import ValidationError
from app.db.session import get_db
from app.services.user_service import _build_user_model

@pytest.fixture()
def client():
    return TestClient(app)

# ===== TDD 테스트 =====

def register_user_for_test(db: Session) -> User:
    existing_user = db.exec(select(User).where(User.email == "testuser@gmail.com")).first()
    if not existing_user:
        new_user = User(username="testuser", email="testuser@gmail.com", password="")
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    return existing_user


def test_get_user_from_social_or_fail_found(db_session):
    register_user_for_test(db_session)
    result = get_user_from_social_or_fail({"email": "testuser@gmail.com"}, "google", db_session)
    assert result.email == "testuser@gmail.com"


def test_get_user_from_social_or_fail_not_found(db_session):
    with pytest.raises(Exception) as err:
        get_user_from_social_or_fail({"email": "notfound@gmail.com"}, "google", db_session)
    assert err.value.status_code == 404


def test_create_user_from_social_info(db_session):
    user_data = {
        "email": "test@gmail.com",
        "username": "Test User",
        "provider": "google"
    }
    register_user = UserSocialCreate(**user_data)

    user = create_user_from_social_info(register_user, db_session)
    assert user.email == "test@gmail.com"
    assert user.username == "Test User"
    assert user.password == ""
    assert user.is_admin is False

def test_social_register_success(db_session, client):
    app.dependency_overrides[get_db] = lambda: db_session

    user_data = {
        "email": "test@gmail.com",
        "username": "Test User",
        "provider": "google"
    }
    user = UserSocialCreate(**user_data)
    response = client.post("/api/v1/users/social-register", json=user.model_dump())
    
    assert response.status_code == 201
    assert response.json()["email"] == user_data["email"]
    assert response.json()["username"] == user_data["username"]

def test_social_register_invalid_provider():
    user_data = {
        "provider": "invalid",
        "email": "testuser@gmail.com",
        "username": "Test User"
    }

    with pytest.raises(ValidationError) as err:
        register_user = UserSocialCreate(**user_data)
        client.post("/api/v1/users/social-register", json=register_user.model_dump())
    
    assert isinstance(err.value, ValidationError)

def test_social_register_missing_email():
    user_data = {
        "provider": "google",
        "username": "Test User"
    }

    with pytest.raises(ValidationError) as err:
        register_user = UserSocialCreate(**user_data)
        client.post("/api/v1/users/social-register", json=register_user.model_dump())
    
    assert isinstance(err.value, ValidationError)
    
def test_social_register_existing_user(db_session : Session, client):
    user_data = {
        "provider": "google",
        "email": "testuser@gmail.com",
        "username": "Test User",
    }
    register_user = UserSocialCreate(**user_data)
    
    user = _build_user_model(email=user_data["email"], username=user_data["username"], provider=user_data["provider"])
    db_session.add(user)
    db_session.commit()
    
    response = client.post("/api/v1/users/social-register", json=register_user.model_dump())
    
    assert response.status_code == 400

# ===== BDD 테스트 =====

@patch("app.api.v1.auth.oauth.google.authorize_access_token", new_callable=AsyncMock)
@patch("app.api.v1.auth.oauth.google.parse_id_token", new_callable=AsyncMock)
def test_google_auth_success(mock_parse_id_token, mock_authorize_access_token, client, db_session):
    # Given: 등록된 OAuth2 사용자
    register_user_for_test(db_session)

    # When: OAuth2 인증 응답 mocking
    mock_authorize_access_token.return_value = {
        "id_token": "abc",
        "userinfo": {"email": "testuser@gmail.com"}
    }
    mock_parse_id_token.return_value = {
        "sub": "google-id-123",
        "email": "testuser@gmail.com",
        "username": "Test User"
    }

    # Then: access_token을 포함한 응답 확인
    response = client.get("/api/v1/oauth2/auth/google")
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@patch("app.api.v1.auth.oauth.google.authorize_access_token", new_callable=AsyncMock)
@patch("app.api.v1.auth.oauth.google.parse_id_token", new_callable=AsyncMock)
def test_google_auth_user_not_found(mock_parse_id_token, mock_authorize_access_token, client, db_session):
    # When: 등록되지 않은 OAuth2 사용자
    mock_authorize_access_token.return_value = {
        "id_token": "test",
        "userinfo": {"email": "notfound@gmail.com"}
    }
    mock_parse_id_token.return_value = {
        "sub": "google-id-1234",
        "email": "notfound@gmail.com",
        "username": "Test User"
    }

    response = client.get("/api/v1/oauth2/auth/google")
    assert response.status_code == 404
