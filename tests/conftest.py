import os
import pytest

from src.start import get_app, get_db, get_project_root, run_startup_tasks


os.environ['FLASK_TESTING'] = '1'
connexion_app = get_app()
database = get_db()
run_startup_tasks(database)


@pytest.fixture(scope='module')
def client():
    with connexion_app.app.test_client() as client:
        yield client
    database_path = get_project_root().joinpath('src', 'db_testing.sqlite')
    database_path.unlink()



