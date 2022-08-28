from pony.orm import db_session

from src.services.create import create_references
from src.start import get_db

db = get_db()


@db_session
def get_all():
    references = db.Reference.select()
    return [ref.to_dict(exclude='timestamp') for ref in references]


def create(references):
    new_instances, errors = create_references(references)
    if errors:
        return {"errors": [e.__str__() for e in errors]}, 409
    return [ref.to_dict(exclude='timestamp') for ref in new_instances], 201
