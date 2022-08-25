import connexion

from src.start import get_db

db = get_db()

def update_game(game, request):
    print(request)
    for key in ["game_types", "game_lengths", "group_sizes"]:
        if key in request.keys():
            update_game_relationships(request, game, key)
    return game

def update_game_relationships(request, game, key):
    for item in getattr(game,key):
        getattr(game,key).remove(item)
    for item in request[key]:
        print(item)
        db_type = {"game_types":"GameType", "game_lengths":"GameLength", "group_sizes":"GroupSize"}
        db_item = getattr(db,db_type[key]).get(slug=item)
        getattr(game,key).add(db_item)

def update_game_bools(request, game):
    pass

def update_game_unique(request, game):
    pass