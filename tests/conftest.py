import functools
import importlib
import os
from pathlib import Path

import pytest
from flask import testing

from pony.orm import *
from werkzeug.datastructures import Headers

from src.start import get_app, get_db, run_startup_tasks


# ToDo: Disable Auth in connexion by patching security.AbstractSecurityHandler
#       Note: monkeypatch only in function-scoped fixture / client is module-scoped
#       Workaround: Use a custom flask.TestClient
# @pytest.fixture(autouse=True)
# def disable_auth(monkeypatch):
#     def mock_verify(cls, auth_funcs, function):
#         @functools.wraps(function)
#         def wrapper(request):
#             return function(request)
#         return wrapper
#
#     from connexion.security.security_handler_factory import AbstractSecurityHandlerFactory
#     monkeypatch.setattr(AbstractSecurityHandlerFactory, "verify_security", mock_verify)


os.environ['FLASK_TESTING'] = '1'
connexion_app = get_app()


def reset_get_db():
    from src.services import create, update, export_to_repo, import_to_db
    from src.views import games, references, api
    importlib.reload(create)
    importlib.reload(update)
    importlib.reload(export_to_repo)
    importlib.reload(import_to_db)
    importlib.reload(games)
    importlib.reload(references)
    importlib.reload(api)


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


@pytest.fixture(scope="module")
def monkeymodule():
    from _pytest.monkeypatch import MonkeyPatch
    mpatch = MonkeyPatch()
    yield mpatch
    mpatch.undo()


@pytest.fixture(scope="module", autouse=True)
def mock_github(monkeymodule):
    def mock_connect():
        return MockRepo()
    from src.services import connect_github
    monkeymodule.setattr(connect_github, "get_repo", mock_connect)


@pytest.fixture(autouse=True)
def mock_import_root(monkeymodule):
    from src.services import import_to_db, connect_github
    test_root = Path(__file__).parent  # /tests
    monkeymodule.setattr(connect_github, "ROOT", test_root)
    monkeymodule.setattr(connect_github, "TMP", test_root.joinpath("resources"))
    monkeymodule.setattr(import_to_db, "TMP", test_root.joinpath("resources"))


@pytest.fixture(scope="module", autouse=True)
def mock_github_token(monkeymodule):
    def mock_get_github_token():
        return "gh1234"
    from src.services import connect_github, import_to_db
    monkeymodule.setattr(connect_github, "get_github_token", mock_get_github_token)
    monkeymodule.setattr(import_to_db, "get_github_token", mock_get_github_token)


@pytest.fixture(scope="module", autouse=True)
def mock_get_sha(monkeymodule, request):
    if "no_mock_get_sha" in request.keywords:
        return
    def mock_get_latest_sha():
        return "1234567"
    from src.services import connect_github
    monkeymodule.setattr(connect_github, "get_latest_sha", mock_get_latest_sha)


@pytest.fixture(scope="module", autouse=True)
def mock_set_sha(monkeymodule, request):
    if "no_mock_set_sha" in request.keywords:
        return
    def mock_set_latest_sha(sha=None):
        pass
    from src.services import connect_github
    monkeymodule.setattr(connect_github, "set_latest_sha", mock_set_latest_sha)


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
        api_key = Headers({"X-Auth": "abc-123"})
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
        with connexion_app.app.app_context():
            yield client
    get_app.cache_clear()
