import re
import unicodedata
from typing import List, Dict

from flask import abort
from pony.orm import db_session
# Pony CacheIndexError when new instance is duplicate/not unique
from pony.orm.core import CacheIndexError

from src.start import get_db

db = get_db()


def slugify(value):
    """Django's slugify - Create an ascii string from unicode
    Convert spaces or repeated dashes to single dashes. Remove characters that aren't alphanumerics, underscores,
    or hyphens. Convert to lowercase. Also strip leading and trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')


@db_session
def create_games(games: List[Dict]):
    """Create one or several new games from the given list and save them in the database.
    """
    created_instances = []
    errors = []

    for game in games:
        game_license = create_game_license(game)
        new_instance = db.Game(license=game_license)
        try:
            set_game_bools(game=new_instance, request=game)
            set_game_categories(game=new_instance, request=game)
            set_game_group_needs(game=new_instance, request=game)
            set_game_names(game=new_instance, request=game)
            set_game_descriptions(game=new_instance, request=game)
            set_game_materials(game=new_instance, request=game)
            set_game_prior_prep(game=new_instance, request=game)
            set_game_meta(game=new_instance, request=game)
        except CacheIndexError as err:
            errors.append(err)
            new_instance.delete()
            continue
        created_instances.append(new_instance)

    return created_instances, errors


def set_game_bools(game, request, keys=('exhausting', 'touching', 'scalable', 'digital')):
    for key in keys:
        game.set(**{key: request[key]})


def set_game_categories(game, request, keys=('game_types', 'game_lengths', 'group_sizes')):
    for key in keys:
        for item in request[key]:
            db_type = {"game_types": "GameType", "game_lengths": "GameLength", "group_sizes": "GroupSize"}
            db_item = getattr(db, db_type[key]).get(slug=item)
            getattr(game, key).add(db_item)


def set_game_group_needs(game, request):
    if request.get('group_needs') is not None:
        for item in request['group_needs']:
            group_need = db.GroupNeed.get(slug=item['slug'])
            db.GroupNeedScore(game=game, group_need=group_need, value=item['score'])


def set_game_names(game, request):
    for item in request['names']:
        slug = slugify(item)
        db.Name.get(slug=slug)  # Needed to flush PonyORM's db_session
        game.names.create(slug=slug, full=item)


def set_game_descriptions(game, request):
    for item in request['descriptions']:
        game.descriptions.create(text=item)


def set_game_materials(game, request):
    if request.get('materials'):
        for item in request['materials']:
            slug = slugify(item)
            existing_item = db.Material.get(slug=slug)
            if existing_item:
                game.materials.add(existing_item)
            else:
                game.materials.create(slug=slug, full=item)


def set_game_prior_prep(game, request):
    if request.get('prior_prep'):
        game.prior_prep = request['prior_prep']


def set_game_meta(game: db.Game, request):
    db.GameMeta(
        game=game,
        author_id=1,  # Todo: Validation with actual User!
    )


def create_game_license(request):
    """Check if the license exists already. Return defaults (from model definition) otherwise.
    """
    if request.get('license'):
        license_url = request['license'].get('url')
        license_owner = request['license'].get('owner')
        license_owner_url = request['license'].get('owner_url')
        if existing := db.License.get(lambda l: l.url == license_url and l.owner == license_owner and l.owner_url == license_owner_url):
            return existing
    return db.License()


@db_session
def create_references(references):
    """Create one or several references from the given list of references and save them to the database.
    """
    created_instances = []
    errors = []

    for ref in references:
        try:
            name = db.Name.get(slug=ref['refers_to'])
            if not name:
                abort(404, description=f"No game with slug {name} to refer to.")
            url = ref.get('url')
            game = name.game
            slug = name.slug + '-ref-' + str(len(game.references))
            new_instance = db.Reference(game=game, slug=slug, full=ref['full'], url=url)
        except CacheIndexError as err:
            errors.append(err)
            continue
        created_instances.append(new_instance)

    return created_instances, errors


@db_session
def create_collections(collections):
    """Create or attach to one or several collections from the given list.
    """
    created_instances = []
    errors = []

    for collection in collections:
        try:
            slug = slugify(collection['full'])
            description = collection.get('description')
            author_id = 1  # Todo: Real Author ID

            instance = db.Collection(slug=slug, full=collection['full'], description=description, author_id=author_id)
            for game in collection.games:
                instance.games.add(game)
            created_instances.append(instance)

        except CacheIndexError as err:
            errors.append(err)
            continue
        created_instances.append(instance)

    return created_instances, errors
