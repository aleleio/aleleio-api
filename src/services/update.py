import connexion

from src.start import get_db

db = get_db()

def update_game(game):
    request = connexion.request.json
    print(request)
    if ("game_types" or "game_length" or "group_size") in request.keys():
        update_game_relationships(request["game_types"], game)
    return game

def update_game_relationships(request, game):
    for item in game.game_types:
        game.game_types.remove(item)
    for item in request:
        game.game_types.add(db.GameType.get(slug=item))

