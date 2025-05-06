import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from app.main import app
from app.db.session import get_db
from app.models.user import User  # SQLModel 기반

DATABASE_URL = "sqlite:///./test.db"  # 테스트용 SQLite

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# DB 세션 의존성 덮어쓰기
def override_get_db():
    with Session(engine) as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

# 테스트용 DB 초기화
@pytest.fixture(scope="session", autouse=True)
def create_test_db():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

@pytest.fixture()
def client():
    return TestClient(app)

@pytest.fixture()
def db_session():
    with Session(engine) as session:
        yield session
