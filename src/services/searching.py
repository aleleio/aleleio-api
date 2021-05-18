from pony.orm import db_session

from src.models import GameQuery, Game, GameOut


def format_game(game):
    game = game.to_dict(with_collections=True, related_objects=True, with_lazy=True, exclude=['statistic', 'versions', 'collections'])
    for item in ['names', 'descriptions']:
        game[item] = [i.to_dict(exclude=['id', 'game'], with_lazy=True) for i in game[item]]
    for item in ['game_types', 'game_lengths', 'group_sizes']:
        game[item] = [i.to_dict(exclude=['id']) for i in game[item]]
    game['group_needs'] = [i.to_dict(exclude=['game'], related_objects=True) for i in game['group_need_scores']]
    for item in game['group_needs']:
        item.update(item['group_need'].to_dict(exclude=['id']))  # extend the dictionary with slug&full
        del item['group_need']
    del game['group_need_scores']
    game['materials'] = [item.to_dict(exclude=['id', 'games']) for item in game['materials']]
    game['meta'] = game['meta'].to_dict(exclude=['id', 'game'])
    game['license'] = game['license'].to_dict(exclude=['id', 'games'])

    print(game)
    return GameOut(
        **game
    )


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

    result = [format_game(game) for game in all_games]

    return result


@db_session
def single_game(game_id: int):
    game = Game.get(id=game_id)
    return format_game(game)