from app.schemas.user import UserCreate
from app.services.user_service import register_user_service, get_user_by_username
from app.models.user import User

def test_create_user_success(db_session):
    register_user = UserCreate(
        username="test123",
        email="test123@mail.com",
        password="test123"
    )
    user = register_user_service(register_user, db_session)

    assert isinstance(user, User)
    assert user.username == "test123"
    assert user.email == "test123@mail.com"
    assert user.password != "test123"
    assert get_user_by_username(db_session, "test123") is not None