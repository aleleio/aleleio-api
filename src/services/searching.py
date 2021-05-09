from pony.orm import db_session

from src.models import GameQuery, Game


@db_session
def all_games(query: GameQuery):
    """Get all games from database, filter by given query and return the amount set by limit.
    Default: Returns all games.
    """
    result = Game.select()
    result.filter(lambda game: query.game_type in game.game_types.slug)
    result.filter(lambda game: query.group_size in game.group_sizes.slug)
    result.filter(lambda game: query.game_length in game.game_lengths.slug)
    result.limit(query.limit)
    return result[:]
