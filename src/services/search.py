from pony.orm import db_session

from src.models import GameQuery, Game, GameORM


@db_session
def all_games(query: GameQuery):
    """Get all games from database, filter by given query and return the amount set by limit.
    Default: Returns all games.
    """
    all_games = Game.select()
    all_games.filter(lambda game: query.game_type in game.game_types.slug)
    all_games.filter(lambda game: query.group_size in game.group_sizes.slug)
    all_games.filter(lambda game: query.game_length in game.game_lengths.slug)
    # Todo: is limit working?
    all_games.limit(query.limit)

    result = [GameORM.from_orm(game) for game in all_games]

    return result
