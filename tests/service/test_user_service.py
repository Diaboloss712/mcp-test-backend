import pytest
from app.crud.user import update_user_fields
from app.schemas.user import UserCreate, UserSocialCreate
from app.services.auth_service import (
    register_user_from_social_info,
    register_user_service,
    get_user_by_username
)
from app.models.user import User
from app.db.session import get_session_factory

class TestUserService:

    @pytest.mark.anyio
    async def test_create_user_success(self):
        session_factory = get_session_factory()
        async with session_factory() as db_session:
            register_dto = UserCreate(
                username="test123",
                email="test123@mail.com",
                password="test123"
            )
            user = await register_user_service(register_dto, db_session)

            # 확정 반영
            await db_session.commit()

            assert isinstance(user, User)
            assert user.username == "test123"
            assert user.email == "test123@mail.com"
            assert user.password != "test123"

            found = await get_user_by_username(db_session, "test123")
            assert found is not None

    @pytest.mark.anyio
    async def test_register_user_from_social_info(self):
        session_factory = get_session_factory()
        async with session_factory() as db_session:
            user_data = {
                "email": "test@gmail.com",
                "username": "Test User",
                "provider": "google"
            }
            register_dto = UserSocialCreate(**user_data)

            user = await register_user_from_social_info(register_dto, db_session)

            await db_session.commit()

            assert user.email == "test@gmail.com"
            assert user.username == "Test User"
            assert user.password == ""
            assert user.is_admin is False

    @pytest.mark.anyio
    async def test_update_user_fields(self, db_session):
        user = User(username="a", email="a@a.com", password="x")
        db_session.add(user)
        await db_session.commit()
        updated_user = await update_user_fields(user, {"username": "b"}, db_session)
        assert updated_user.username == "b"
