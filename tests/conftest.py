import pytest
import connexion
from src.start import get_app

flask_app = get_app()


@pytest.fixture(scope='module')
def client():
    with flask_app.app.test_client() as client:
        yield client
