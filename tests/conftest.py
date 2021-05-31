import pytest

from fastapi.testclient import TestClient
from pony.orm import Database

from src.main import configure, application as app
from src.models import define_entities_game, define_entities_meta, define_entities_user


# default is: @fixture(scope='function')

def teardown(db):
    print('TEARING DOWN ', db)
    db.drop_all_tables(with_all_data=True)
    db.disconnect()
    db.provider = None
    db.schema = None


@pytest.fixture()
def db():
    database = Database('sqlite', ':memory:')
    define_entities_game(database)
    define_entities_meta(database)
    define_entities_user(database)
    database.generate_mapping(create_tables=True)
    return database


@pytest.fixture()
def client(db):
    client = TestClient(app)
    configure(app, db)
    yield client
    teardown(db)
