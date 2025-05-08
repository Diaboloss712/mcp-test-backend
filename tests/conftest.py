import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from app.main import app
from app.db.session import get_db
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=False)

@pytest.fixture(autouse=True)
def clean_db():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

@pytest.fixture()
def db_session():
    with Session(engine) as session:
        app.dependency_overrides[get_db] = lambda: session
        yield session

@pytest.fixture()
def client():
    return TestClient(app)
