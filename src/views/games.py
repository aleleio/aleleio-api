from typing import List, Dict

from flask import abort
from pony.orm import db_session

from src.services.create import create_games
from src.start import get_db

db = get_db()


@db_session
def get_all():
    games = db.Game.select()
    result = [g.to_dict() for g in games]
    return result


@db_session
def create(games: List[Dict]):
    create_games(games)
    return [], 201


@db_session
def get_single(game_id):
    game = db.Game.get(id=game_id)
    if game is None:
        abort(404)
    return game.to_dict()


def update_single():
    return "update_single"


def delete_single():
    return "delete_single"