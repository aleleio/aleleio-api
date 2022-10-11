import functools
from importlib import reload
import os
from pathlib import Path

import pytest
from _pytest.monkeypatch import MonkeyPatch
from flask import testing
from pony.orm import *
from werkzeug.datastructures import Headers

from src.services import authentication, search, tracking, create, export_to_repo, update
from src.start import get_app, get_db, run_startup_tasks
from src.views import collections, games, references

os.environ['FLASK_TESTING'] = '1'


@pytest.fixture(scope="module")
def monkeymodule():
    """Monkeypatch with module scope
    """
    mpatch = MonkeyPatch()
    yield mpatch
    mpatch.undo()


@pytest.fixture(scope='module')
def db(monkeymodule):
    """
    Painful learning:
    - Reload modules for the refreshed Singleton (get_db.cache_clear) to take effect when testing multiple modules.
    """
    db = get_db()
    udb = get_db(users_db=True)

    for module in [authentication, tracking, search, create, update, export_to_repo, games, collections, references]:
        reload(module)

    from src.services import connect_github
    from tests.mocks import mock_get_latest_commit
    monkeymodule.setattr(connect_github, "get_latest_commit", mock_get_latest_commit)

    run_startup_tasks(db)
    run_startup_tasks(udb)
    add_test_users(udb)

    yield db

    get_db.cache_clear()

    for d in [db, udb]:
        d.drop_all_tables(with_all_data=True)
        d.disconnect()


@db_session
def add_test_users(udb):
    """Add test_user and CustomTestClient to provide Connexion Authentication
    """
    udb.User(**{"login": "test_user", "created_by": 1, "api_key": "abc-123", "hashed_password": "test", "role": "editor", "status": "active"})


@pytest.fixture(scope='module')
def no_auth_client(db):
    connexion_app = get_app()
    connexion_app.app.test_client_class = testing.FlaskClient
    with connexion_app.app.test_client() as client:
        yield client
    get_app.cache_clear()


@pytest.fixture(scope='module')
def client(db):
    connexion_app = get_app()
    class CustomTestClient(testing.FlaskClient):
        def open(self, *args, **kwargs):
            api_key = Headers({"X-Auth": "abc-123"})
            headers = kwargs.pop("headers", Headers())
            headers.extend(api_key)
            kwargs["headers"] = headers
            return super().open(*args, **kwargs)
    connexion_app.app.test_client_class = CustomTestClient
    with connexion_app.app.test_client() as client:
        with connexion_app.app.app_context():
            yield client
    get_app.cache_clear()


@pytest.fixture(autouse=True)
def mocks(monkeypatch):
    from src.services import import_to_db, export_to_repo
    from tests.mocks import mock_get_github_token, mock_get_latest_sha, mock_get_repo
    monkeypatch.setattr(export_to_repo, "get_repo", mock_get_repo)
    monkeypatch.setattr(import_to_db, "get_github_token", mock_get_github_token)
    monkeypatch.setattr(import_to_db, "get_latest_sha", mock_get_latest_sha)


@pytest.fixture(autouse=True)
def mock_import_root(monkeypatch):
    from src.services import import_to_db, connect_github
    test_root = Path(__file__).parent  # /tests
    monkeypatch.setattr(connect_github, "TMP", test_root.joinpath("resources"))
    monkeypatch.setattr(import_to_db, "TMP", test_root.joinpath("resources"))

