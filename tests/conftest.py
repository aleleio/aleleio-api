import importlib
import os
import pytest

from src.start import get_app, get_db, get_project_root, run_startup_tasks

os.environ['FLASK_TESTING'] = '1'
connexion_app = get_app()


def reset_db_get():
    import src.services.create
    importlib.reload(src.services.create)
    import src.services.update
    importlib.reload(src.services.update)


@pytest.fixture(scope='module')
def db():
    database = get_db()
    reset_db_get()
    run_startup_tasks(database)
    yield database
    get_db.cache_clear()
    database.drop_all_tables(with_all_data=True)
    database.disconnect()

    # database_path = get_project_root().joinpath('src', 'db_testing.sqlite')
    # database_path.unlink()


@pytest.fixture(scope='module')
def client(db):
    with connexion_app.app.test_client() as client:
        yield client
    get_app.cache_clear()
