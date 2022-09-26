from pony.orm import CacheIndexError, select

from src.services import create
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


def update_diff(game, request, key):
    if key == "descriptions":
        old_set = set(select(k.text for k in getattr(game, key))[:])
    else:
        old_set = set(select(k.full for k in getattr(game, key))[:])
    new_set = set(request[key])
    added = new_set - old_set
    deleted = old_set - new_set
    return list(added), list(deleted)


def update_game_names(game, request):
    """Update the requested changes for names without changing the db.Name creation IDs.
    Store deleted games in request[] to enable export to teambuilding-games repository.
    """
    if "names" in request.keys():
        added, deleted = update_diff(game, request, key="names")
        if added:
            request["names"] = added
            create.set_game_names(game, request)
        else:
            del request["names"]
        if deleted:
            request["names_deleted"] = list()
            for name in deleted:
                dead_name = db.Name.get(full=name)
                request["names_deleted"].append(dict(id=dead_name.id, slug=dead_name.slug))
                dead_name.delete()  # delete at last moment, else problems with duplicate name exceptions


def update_game_descriptions(game, request):
    if "descriptions" in request.keys():
        added, deleted = update_diff(game, request, key="descriptions")
        if added:
            request["descriptions"] = added
            create.set_game_descriptions(game, request)
        else:
            del request["descriptions"]
        if deleted:
            for item in deleted:
                dead_item = db.Description.get(text=item)
                dead_item.delete()


def update_game_materials(game, request):
    create.set_game_materials(game, request)


def update_game_prior_prep(game, request):
    create.set_game_prior_prep(game, request)


def update_game_license(game, request):
    if "license" in request.keys():
        new_license = create.create_game_license(request)
        game.license = new_license
