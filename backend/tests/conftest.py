import pytest

from app.main import app
from app.db.base import Base
from app.db.database import engine
from app.services.storage_service import get_storage

from tests.fakes.fake_storage import FakeStorage


@pytest.fixture(scope="session", autouse=True)
def create_test_database():

    Base.metadata.create_all(bind=engine)

    yield

    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def fake_storage():

    storage = FakeStorage()

    app.dependency_overrides[get_storage] = lambda: storage

    yield storage

    app.dependency_overrides.clear()