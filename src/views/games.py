from typing import List, Dict

import connexion
from flask import abort
from pony.orm import db_session

from src.services import search, export
from src.services.create import create_games
from src.services.update import update_game
from src.start import get_db

db = get_db()


def get_all():
    query = connexion.request.values
    return search.all_games(query)


def create(games: List[Dict]):
    new_instances, errors = create_games(games)
    if errors:
        return {"errors": [e.__str__() for e in errors]}, 409
    export.create_multiple_games(new_instances)
    return [game.to_schema_out() for game in new_instances], 201


@db_session
def get_single(game_id):
    game = db.Game.get(id=game_id)
    if game is None:
        abort(404)
    return game.to_schema_out()


@db_session
def update_single(game_id, patch):
    game = db.Game.get(id=game_id)
    if game is None:
        abort(404)
    game, errors = update_game(game, patch)
    if errors:
        return {"errors": [e.__str__() for e in errors]}, 409
    export.update_single_game(game, patch)
    return game.to_schema_out()


@db_session
def delete_single(game_id):
    game = db.Game.get(id=game_id)
    if game is None:
        abort(404)
    export.delete_game(game)
    for name in game.names:
        name.delete()
    game.delete()
    return {"success": f"Deleted game#{game_id}."}
