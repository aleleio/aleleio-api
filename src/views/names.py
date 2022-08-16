import connexion
from pony.orm import db_session

from src.services import search
from src.start import get_db

db = get_db()


@db_session()
def get_all():
    query = connexion.request.values
    return search.all_names(query)
