from pony.orm import CacheIndexError, select

from src.services import create
from src.services.create import slugify
from src.start import get_db

db = get_db()


def update_game(game, request):
    errors = []
    try:
        update_game_bools(game, request)
        update_game_categories(game, request)
        update_game_group_needs(game, request)
        update_game_names(game, request)
        update_game_descriptions(game, request)
        update_game_materials(game, request)
        update_game_prior_prep(game, request)
        update_game_license(game, request)
    except CacheIndexError as err:
        errors.append(err)
    return game, errors


def update_game_bools(game, request):
    keys = [key for key in ["exhausting", "touching", "scalable", "digital"] if key in request.keys()]
    create.set_game_bools(game, request, keys=keys)


def update_game_categories(game, request):
    keys = [key for key in ["game_types", "game_lengths", "group_sizes"] if key in request.keys()]
    for key in keys:
        getattr(game, key).clear()
    create.set_game_categories(game, request, keys=keys)


def update_game_group_needs(game, request):
    if "group_needs" in request.keys():
        game.group_need_scores.clear()
        create.set_game_group_needs(game, request)


def update_game_names(game, request):
    """Update the requested changes for names without changing the db.Name creation IDs.
    game.names.clear() would delete not only the connection but also the db.Name entries
    themselves because of the Required() property.
    """
    if "names" in request.keys():
        old_nameset = set(select(n.full for n in game.names)[:])
        new_nameset = set(request["names"])
        names_deleted = old_nameset - new_nameset
        names_new = new_nameset - old_nameset

        if names_deleted:
            request["names_deleted"] = list()
            for name in names_deleted:
                dead_name = db.Name.get(full=name)
                request["names_deleted"].append(dead_name.id)
                dead_name.delete()

        if names_new:
            request["names"] = list(names_new)
            create.set_game_names(game, request)



def update_game_descriptions(game, request):
    if "descriptions" in request.keys():
        game.descriptions.clear()
        create.set_game_descriptions(game, request)


def update_game_materials(game, request):
    create.set_game_materials(game, request)


def update_game_prior_prep(game, request):
    create.set_game_prior_prep(game, request)


def update_game_license(game, request):
    if "license" in request.keys():
        new_license = create.create_game_license(request)
        game.license = new_license
