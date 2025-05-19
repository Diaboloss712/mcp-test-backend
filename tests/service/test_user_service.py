import pytest
from app.schemas.user import UserCreate, UserSocialCreate
from app.services.user_service import (
    register_user_from_social_info,
    register_user_service,
    get_user_by_username
)
from app.models.user import User
from app.db.session import SessionFactory

@pytest.mark.anyio
class TestUserService:

    async def test_create_user_success(self, client, db_session):
        # client 내부의 session을 공유
        async with SessionFactory() as db_session:
            register_dto = UserCreate(
                username="test123",
                email="test123@mail.com",
                password="test123"
            )
            user = await register_user_service(register_dto, db_session)

            assert isinstance(user, User)
            assert user.username == "test123"
            assert user.email == "test123@mail.com"
            assert user.password != "test123"

            found = await get_user_by_username(db_session, "test123")
            assert found is not None

    async def test_register_user_from_social_info(self, client):
        async with SessionFactory() as db_session:
            user_data = {
                "email": "test@gmail.com",
                "username": "Test User",
                "provider": "google"
            }
            register_dto = UserSocialCreate(**user_data)

            user = await register_user_from_social_info(register_dto, db_session)

            assert user.email == "test@gmail.com"
            assert user.username == "Test User"
            assert user.password == ""
            assert user.is_admin is False
