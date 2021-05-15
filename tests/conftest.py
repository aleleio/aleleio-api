import pytest

from fastapi.testclient import TestClient

# default is: fixture(scope='function')
from src.main import api as app, configure


@pytest.fixture(scope='session')
def client():
    client = TestClient(app)
    configure()
    return client


@pytest.fixture()
def database():
    pass
