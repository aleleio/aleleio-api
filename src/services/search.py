from enum import Enum

from pony.orm import db_session

from src.start import get_db

QUERY_PARAMS = ["game_type", "game_length", "group_size", "main", "aux1", "aux2", "limit"]
db = get_db()


@db_session
def all_games(query: dict):
    """Get all games from database, filter by given query and return the amount set by limit.
    Default: Returns all games.
    """

    games = db.Game.select()
    if game_type := query.get('game_type'):
        games = games.filter(lambda game: game_type in game.game_types.slug)
    if group_size := query.get('group_size'):
        games = games.filter(lambda game: group_size in game.group_sizes.slug)
    if game_length := query.get('game_length'):
        games = games.filter(lambda game: game_length in game.game_lengths.slug)
    if limit := query.get('limit'):
        games = games.limit(int(limit))

    result = [game.to_schema_out() for game in games]

    return result
