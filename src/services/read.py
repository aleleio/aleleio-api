from pony.orm import db_session

from src.models import GameOut, Game, Reference


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
def single_game(game_id: int):
    game = Game.get(id=game_id)
    return format_game(game)


@db_session
def all_references():
    refs = Reference.select()
    return refs[:]