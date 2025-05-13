# tests/api/v1/test_user_api.py
import pytest
from unittest.mock import AsyncMock, patch

from app.schemas.user import UserSocialCreate
from app.services.user_service import _build_user_model
from app.crud.user import update_user_fields

@pytest.mark.anyio
async def test_social_register_success(client):
    data = {"email": "test@gmail.com", "username": "Test User", "provider": "google"}
    body = UserSocialCreate(**data)
    r = await client.post("/api/v1/users/social-register", json=body.model_dump())
    assert r.status_code == 201

def test_social_register_invalid_provider():
    with pytest.raises(ValueError):
        UserSocialCreate(provider="invalid", email="x@x.com", username="X")

def test_social_register_missing_email():
    with pytest.raises(ValueError):
        UserSocialCreate(provider="google", username="X")

@pytest.mark.anyio
async def test_social_register_existing_user(client):
    data = {"email": "dup@e.com", "username": "Dup", "provider": "google"}
    r1 = await client.post("/api/v1/users/social-register", json=data)
    assert r1.status_code == 201
    r2 = await client.post("/api/v1/users/social-register", json=data)
    assert r2.status_code == 400
    assert r2.json()["detail"] == "User already exists"

@pytest.mark.anyio
async def test_signup_user_success(client):
    payload = {"username": "test1", "email": "test1@test.com", "password": "test1"}
    r = await client.post("/api/v1/users/register", json=payload)
    assert r.status_code == 201
    j = r.json()
    assert j["username"] == payload["username"]
    assert j["email"] == payload["email"]
    assert "password" not in j

@pytest.mark.anyio
async def test_register_user_duplicate_username(client):
    await client.post("/api/v1/users/register", json={"username": "dup", "email": "a@a.com", "password": "x"})
    r = await client.post("/api/v1/users/register", json={"username": "dup", "email": "b@b.com", "password": "y"})
    assert r.status_code == 400
    assert r.json()["detail"] == "Username already taken"

@pytest.mark.anyio
async def test_register_user_duplicate_email(client):
    await client.post("/api/v1/users/register", json={"username": "u1", "email": "dup@e.com", "password": "x"})
    r = await client.post("/api/v1/users/register", json={"username": "u2", "email": "dup@e.com", "password": "y"})
    assert r.status_code == 400
    assert r.json()["detail"] == "Email already taken"

@pytest.mark.anyio
async def test_login_user_success(client):
    await client.post("/api/v1/users/register", json={"username": "L", "email": "l@test.com", "password": "pw"})
    r = await client.post("/api/v1/users/login", data={"username": "L", "password": "pw"})
    assert r.status_code == 200
    j = r.json()
    assert "access_token" in j and j["token_type"] == "bearer"

@pytest.mark.anyio
async def test_login_user_invalid_password(client):
    await client.post("/api/v1/users/register", json={"username": "L2", "email": "l2@test.com", "password": "pw"})
    r = await client.post("/api/v1/users/login", data={"username": "L2", "password": "wrong"})
    assert r.status_code == 401
    assert r.json()["detail"] == "Incorrect username or password"

@pytest.mark.anyio
async def test_google_auth_success(client, override_get_db):
    # DB에 유저 직접 추가
    async for session in override_get_db():
        u = _build_user_model(email="testuser@gmail.com", username="TU", password="")
        session.add(u)
        await session.commit()
        break

    with patch("app.api.v1.auth.oauth.google.authorize_access_token", new_callable=AsyncMock) as mock_token, \
         patch("app.api.v1.auth.oauth.google.parse_id_token",     new_callable=AsyncMock) as mock_parse:

        mock_token.return_value = {"id_token": "t", "userinfo": {"email": "testuser@gmail.com"}}
        mock_parse.return_value = {"sub": "g123", "email": "testuser@gmail.com", "username": "TU"}

        r = await client.get("/api/v1/oauth2/auth/google")
        assert r.status_code == 200
        assert "access_token" in r.json()

@pytest.mark.anyio
async def test_google_auth_user_not_found(client):
    with patch("app.api.v1.auth.oauth.google.authorize_access_token", new_callable=AsyncMock) as mock_token, \
         patch("app.api.v1.auth.oauth.google.parse_id_token",     new_callable=AsyncMock) as mock_parse:

        mock_token.return_value = {"id_token": "t", "userinfo": {"email": "no@no.com"}}
        mock_parse.return_value = {"sub": "g456", "email": "no@no.com", "username": "Nobody"}

        r = await client.get("/api/v1/oauth2/auth/google")
        assert r.status_code == 404

@pytest.mark.anyio
async def test_update_user_profile_success(client):
    await client.post("/api/v1/users/register", json={"username": "P", "email": "p@test.com", "password": "pw"})
    login = await client.post("/api/v1/users/login", data={"username": "P", "password": "pw"})
    tok = login.json()["access_token"]
    r = await client.patch(
        "/api/v1/users/profile/update",
        headers={"Authorization": f"Bearer {tok}"},
        json={"username": "P2"}
    )
    assert r.status_code == 200
    assert r.json()["username"] == "P2"

@pytest.mark.anyio
async def test_get_user_profile_success(client):
    await client.post("/api/v1/users/register", json={"username": "Q", "email": "q@test.com", "password": "pw"})
    login = await client.post("/api/v1/users/login", data={"username": "Q", "password": "pw"})
    tok = login.json()["access_token"]
    r = await client.get("/api/v1/users/profile", headers={"Authorization": f"Bearer {tok}"})
    assert r.status_code == 200
    assert r.json()["email"] == "q@test.com"

@pytest.mark.anyio
async def test_login_user_not_found(client):
    r = await client.post("/api/v1/users/login", data={"username": "nouser", "password": "nopass"})
    assert r.status_code == 401

@pytest.mark.anyio
async def test_update_user_fields(override_get_db):
    async for session in override_get_db():
        from app.models.user import User
        u = User(username="a", email="a@a.com", password="x")
        session.add(u)
        await session.commit()
        updated = await update_user_fields(u, {"username": "b"}, session)
        assert updated.username == "b"
        break
