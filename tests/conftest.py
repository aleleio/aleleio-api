import importlib
import os
from pathlib import Path

import pytest
from flask import testing

from pony.orm import *
from werkzeug.datastructures import Headers

from src.start import get_app, get_db, run_startup_tasks, ROOT

os.environ['FLASK_TESTING'] = '1'
connexion_app = get_app()


def reset_get_db():
    import src.services.create
    importlib.reload(src.services.create)
    import src.services.update
    importlib.reload(src.services.update)
    import src.services.export_to_repo
    importlib.reload(src.services.export_to_repo)
    import src.views.games
    importlib.reload(src.views.games)


class MockRepo:
    class Blob:
        def __init__(self):
            self.sha = '12345abc'

    def create_git_blob(self, content, encoding):
        return self.Blob()

    class InputTreeGitElement:
        pass

    class Commit:
        def __init__(self):
            self.sha = '12345abc'

    class Branch:
        def __init__(self, ref):
            self.ref = ref

        @property
        def commit(self):
            return MockRepo.Commit()

    def get_branch(self, ref):
        return self.Branch(ref)

    @staticmethod
    def get_git_tree(sha):
        return 'base_tree'

    @staticmethod
    def create_git_tree(element_list, base_tree):
        return 'tree'

    @staticmethod
    def get_git_commit(sha):
        return 'parent'

    def create_git_commit(self, message, tree, parents):
        return self.Commit()

    class Reference:
        @staticmethod
        def edit(sha):
            return 'branch_refs'

    def get_git_ref(self, path):
        return self.Reference


@pytest.fixture(autouse=True)
def mock_github(monkeypatch):
    def mock_connect():
        return MockRepo()
    from src.services import export_to_repo
    monkeypatch.setattr(export_to_repo, "get_repo", mock_connect)


@pytest.fixture(autouse=True)
def mock_import_root(monkeypatch):
    from src.services import import_to_db
    monkeypatch.setattr(import_to_db, "TMP", ROOT.joinpath("tests", "resources"))


@pytest.fixture(autouse=True)
def mock_get_sha(monkeypatch, request):
    if "no_mock_get_sha" in request.keywords:
        return
    def mock_get_latest_sha():
        return "1234567"
    from src.services import import_to_db
    monkeypatch.setattr(import_to_db, "get_latest_sha", mock_get_latest_sha)


@pytest.fixture(autouse=True)
def mock_set_sha(monkeypatch, request):
    if "no_mock_set_sha" in request.keywords:
        return
    def mock_set_latest_sha(sha):
        pass
    from src.services import export_to_repo
    monkeypatch.setattr(export_to_repo, "set_latest_sha", mock_set_latest_sha)


@pytest.fixture(scope='module')
def db():
    db = get_db()
    udb = get_db(users_db=True)
    reset_get_db()
    run_startup_tasks(db)
    add_test_users(udb)
    yield db
    get_db.cache_clear()
    db.drop_all_tables(with_all_data=True)
    db.disconnect()
    udb.drop_all_tables(with_all_data=True)
    udb.disconnect()

    # database_path = ROOT.joinpath('src', 'db_api_testing.sqlite')
    # database_path.unlink()


@db_session
def add_test_users(udb):
    udb.User(**{"login": "test_user", "created_by": 1, "api_key": "abc-123", "hashed_password": "test", "role": "editor", "status": "active"})


class CustomTestClient(testing.FlaskClient):
    def open(self, *args, **kwargs):
        api_key = Headers({"Authorization": "Basic abc-123"})
        headers = kwargs.pop("headers", Headers())
        headers.extend(api_key)
        kwargs["headers"] = headers
        return super().open(*args, **kwargs)


@pytest.fixture(scope='module')
def no_auth_client(db):
    connexion_app.app.test_client_class = testing.FlaskClient
    with connexion_app.app.test_client() as client:
        yield client
    get_app.cache_clear()


@pytest.fixture(scope='module')
def client(db):
    connexion_app.app.test_client_class = CustomTestClient
    with connexion_app.app.test_client() as client:
        yield client
    get_app.cache_clear()


