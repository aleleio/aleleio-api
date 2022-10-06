from flask import request
from pony.orm import db_session

from src.services import search


@db_session()
def get_all():
    query = request.values
    return search.all_names(query)
