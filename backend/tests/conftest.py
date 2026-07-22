import pytest

from app.main import app
from app.services.storage_service import get_storage

from tests.fakes.fake_storage import FakeStorage


@pytest.fixture
def fake_storage():

    storage = FakeStorage()

    app.dependency_overrides[get_storage] = lambda: storage

    yield storage

    app.dependency_overrides.clear()