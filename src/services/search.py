from pony.orm import db_session, select

from src.start import get_db

db = get_db()


@db_session()
def all_games(query: dict):
    """Get all games from database, filter by given query and return the amount set by limit.
    Default: Returns all games.
    """
    games = db.Game.select()
    games = filter_games_query(games, query)
    if query.get('main'):
        games = add_weights_to_query(games, query)
        games = [game.to_schema_out() for game in games]
        games.sort(key=lambda x: x['weight'])
        games.reverse()
    else:
        games = [game.to_schema_out() for game in games]

    if limit := query.get('limit'):
        games = games[:int(limit)]

    return games


@db_session()
def all_names(query: dict):
    """Get all game names from database, and filter by given query.
    Used by Web Component to show filtered list of games.
    """
    names = db.Name.select()
    names = filter_names_query(names, query)
    if query.get('main'):
        names = add_weights_to_query(names, query, caller='names')
        names = [name.to_schema_out() for name in names]
        names.sort(key=lambda x: x['weight'])
        names.reverse()
    else:
        names = [name.to_schema_out() for name in names]

    if limit := query.get('limit'):
        names = names[:int(limit)]

    return names


def filter_games_query(games, query):
    if game_type := query.get('game_type'):
        games = games.filter(lambda game: game_type in game.game_types.slug)
    if group_size := query.get('group_size'):
        games = games.filter(lambda game: group_size in game.group_sizes.slug)
    if game_length := query.get('game_length'):
        games = games.filter(lambda game: game_length in game.game_lengths.slug)

    if gn_main := query.get('main'):
        games = games.filter(lambda game: gn_main in game.group_need_scores.group_need.slug)

    return games


def filter_names_query(names, query):
    if game_type := query.get('game_type'):
        names = names.filter(lambda name: game_type in name.game.game_types.slug)
    if group_size := query.get('group_size'):
        names = names.filter(lambda name: group_size in name.game.group_sizes.slug)
    if game_length := query.get('game_length'):
        names = names.filter(lambda name: game_length in name.game.game_lengths.slug)

    if gn_main := query.get('main'):
        names = names.filter(lambda name: gn_main in name.game.group_need_scores.group_need.slug)

    return names


def add_weights_to_query(db_result, query, caller='games'):
    main = query.get('main')
    aux1 = query.get('aux1')
    aux2 = query.get('aux2')

    for item in db_result:
        game = item.game if (caller == 'names') else item

        main_val = select(s.value for s in db.GroupNeedScore if s.game == game and s.group_need.slug == main).get()
        aux1_val = select(s.value for s in db.GroupNeedScore if s.game == game and s.group_need.slug == aux1).get()
        aux2_val = select(s.value for s in db.GroupNeedScore if s.game == game and s.group_need.slug == aux2).get()
        item.weight = (main_val or 0) * 1.5 + (aux1_val or 0) + (aux2_val or 0)

    return db_result
