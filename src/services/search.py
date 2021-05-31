from pony.orm import db_session

from src.main import database as db
from src.models import GameQuery, GameORM


@db_session
def all_games(query: GameQuery):
    """Get all games from database, filter by given query and return the amount set by limit.
    Default: Returns all games.
    """
    games = db.Game.select()
    games.filter(lambda game: query.game_type in game.game_types.slug)
    games.filter(lambda game: query.group_size in game.group_sizes.slug)
    games.filter(lambda game: query.game_length in game.game_lengths.slug)
    # Todo: is limit working?
    games.limit(query.limit)

    result = [GameORM.from_orm(game) for game in games]

    return result
