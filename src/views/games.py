import os
from typing import List, Dict

import connexion
from flask import abort
from pony.orm import db_session

from src.services import search
from src.services.create import create_games
from src.start import get_db

db = get_db()


@db_session
def get_all():
    query = connexion.request.values
    result = search.all_games(query)
    # games = db.Game.select()[:]
    # result = [game.to_schema_out() for game in games]
    return result


@db_session
def create(games: List[Dict]):
    new_instances, errors = create_games(games)
    if errors:
        return {"errors": [e.__str__() for e in errors]}, 409
    return [game.to_schema_out() for game in new_instances], 201


@db_session
def get_single(game_id):
    game = db.Game.get(id=game_id)
    if game is None:
        abort(404)
    return game.to_schema_out()


def update_single():
    return "update_single"


def delete_single():
    return "delete_single"