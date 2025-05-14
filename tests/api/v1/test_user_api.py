import pytest
from unittest.mock import AsyncMock, patch

from app.schemas.user import UserSocialCreate
from app.services.user_service import _build_user_model
from app.crud.user import update_user_fields
from app.models.user import User


class TestUserAPI:

    @pytest.mark.anyio
    async def test_social_register_success(self, client):
        user_data = {"email": "test@gmail.com", "username": "Test User", "provider": "google"}
        request_body = UserSocialCreate(**user_data)
        response = await client.post("/api/v1/users/social-register", json=request_body.model_dump())
        assert response.status_code == 201

    def test_social_register_invalid_provider(self):
        with pytest.raises(ValueError):
            UserSocialCreate(provider="invalid", email="x@x.com", username="X")

    def test_social_register_missing_email(self):
        with pytest.raises(ValueError):
            UserSocialCreate(provider="google", username="X")

    @pytest.mark.anyio
    async def test_social_register_existing_user(self, client):
        user_data = {"email": "dup@e.com", "username": "Dup", "provider": "google"}
        first_response = await client.post("/api/v1/users/social-register", json=user_data)
        assert first_response.status_code == 201

        duplicate_response = await client.post("/api/v1/users/social-register", json=user_data)
        assert duplicate_response.status_code == 400
        assert duplicate_response.json()["detail"] == "User already exists"

    @pytest.mark.anyio
    async def test_signup_user_success(self, client):
        signup_payload = {"username": "test1", "email": "test1@test.com", "password": "test1"}
        response = await client.post("/api/v1/users/register", json=signup_payload)
        assert response.status_code == 201

        response_data = response.json()
        assert response_data["username"] == signup_payload["username"]
        assert response_data["email"] == signup_payload["email"]
        assert "password" not in response_data

    @pytest.mark.anyio
    async def test_register_user_duplicate_username(self, client):
        await client.post("/api/v1/users/register", json={"username": "dup", "email": "a@a.com", "password": "x"})
        response = await client.post("/api/v1/users/register", json={"username": "dup", "email": "b@b.com", "password": "y"})
        assert response.status_code == 400
        assert response.json()["detail"] == "Username already taken"

    @pytest.mark.anyio
    async def test_register_user_duplicate_email(self, client):
        await client.post("/api/v1/users/register", json={"username": "u1", "email": "dup@e.com", "password": "x"})
        response = await client.post("/api/v1/users/register", json={"username": "u2", "email": "dup@e.com", "password": "y"})
        assert response.status_code == 400
        assert response.json()["detail"] == "Email already taken"

    @pytest.mark.anyio
    async def test_login_user_success(self, client):
        await client.post("/api/v1/users/register", json={"username": "L", "email": "l@test.com", "password": "pw"})
        login_response = await client.post("/api/v1/users/login", data={"username": "L", "password": "pw"})
        assert login_response.status_code == 200

        token_data = login_response.json()
        assert "access_token" in token_data and token_data["token_type"] == "bearer"

    @pytest.mark.anyio
    async def test_login_user_invalid_password(self, client):
        await client.post("/api/v1/users/register", json={"username": "L2", "email": "l2@test.com", "password": "pw"})
        invalid_login_response = await client.post("/api/v1/users/login", data={"username": "L2", "password": "wrong"})
        assert invalid_login_response.status_code == 401
        assert invalid_login_response.json()["detail"] == "Incorrect username or password"

    @pytest.mark.anyio
    async def test_login_user_not_found(self, client):
        login_response = await client.post("/api/v1/users/login", data={"username": "nouser", "password": "nopass"})
        assert login_response.status_code == 401

    @pytest.mark.anyio
    async def test_google_auth_success(self, client, db_session):
        async with db_session as session:
            test_user = _build_user_model(email="testuser@gmail.com", username="TU", password="")
            session.add(test_user)
            await session.commit()

        with patch("app.api.v1.auth.oauth.google.authorize_access_token", new_callable=AsyncMock) as mock_token, \
             patch("app.api.v1.auth.oauth.google.parse_id_token", new_callable=AsyncMock) as mock_parse:

            mock_token.return_value = {"id_token": "t", "userinfo": {"email": "testuser@gmail.com"}}
            mock_parse.return_value = {"sub": "g123", "email": "testuser@gmail.com", "username": "TU"}

            auth_response = await client.get("/api/v1/oauth2/auth/google")
            assert auth_response.status_code == 200
            assert "access_token" in auth_response.json()

    @pytest.mark.anyio
    async def test_google_auth_user_not_found(self, client):
        with patch("app.api.v1.auth.oauth.google.authorize_access_token", new_callable=AsyncMock) as mock_token, \
             patch("app.api.v1.auth.oauth.google.parse_id_token", new_callable=AsyncMock) as mock_parse:

            mock_token.return_value = {"id_token": "t", "userinfo": {"email": "no@no.com"}}
            mock_parse.return_value = {"sub": "g456", "email": "no@no.com", "username": "Nobody"}

            auth_response = await client.get("/api/v1/oauth2/auth/google")
            assert auth_response.status_code == 404

    @pytest.mark.anyio
    async def test_update_user_profile_success(self, client):
        await client.post("/api/v1/users/register", json={"username": "P", "email": "p@test.com", "password": "pw"})
        login_response = await client.post("/api/v1/users/login", data={"username": "P", "password": "pw"})
        access_token = login_response.json()["access_token"]

        update_response = await client.patch(
            "/api/v1/users/profile/update",
            headers={"Authorization": f"Bearer {access_token}"},
            json={"username": "P2"}
        )
        assert update_response.status_code == 200
        assert update_response.json()["username"] == "P2"

    @pytest.mark.anyio
    async def test_get_user_profile_success(self, client):
        await client.post("/api/v1/users/register", json={"username": "Q", "email": "q@test.com", "password": "pw"})
        login_response = await client.post("/api/v1/users/login", data={"username": "Q", "password": "pw"})
        access_token = login_response.json()["access_token"]

        profile_response = await client.get("/api/v1/users/profile", headers={"Authorization": f"Bearer {access_token}"})
        assert profile_response.status_code == 200
        assert profile_response.json()["email"] == "q@test.com"

    @pytest.mark.anyio
    async def test_update_user_fields(self, db_session):
        async with db_session as session:
            user = User(username="a", email="a@a.com", password="x")
            session.add(user)
            await session.commit()
            updated_user = await update_user_fields(user, {"username": "b"}, session)
            assert updated_user.username == "b"
