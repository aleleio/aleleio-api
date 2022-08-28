from pony.orm import db_session

from src.start import get_db

db = get_db()


@db_session
def get_all():
    collections = db.Collection.select()
    return [c.to_dict(with_collections=True) for c in collections]


def create():
    pass
