import importlib
import os
import pytest

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
        def __init__(self, path, mode, type, sha):
            self.path = path
            self.mode = mode
            self.type = type
            self.sha = sha

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


@pytest.fixture(scope='module')
def db():
    database = get_db()
    reset_get_db()
    run_startup_tasks(database)
    yield database
    get_db.cache_clear()
    database.drop_all_tables(with_all_data=True)
    database.disconnect()

    # database_path = ROOT.joinpath('src', 'db_api_testing.sqlite')
    # database_path.unlink()


@pytest.fixture(scope='module')
def client(db):
    with connexion_app.app.test_client() as client:
        yield client
    get_app.cache_clear()
