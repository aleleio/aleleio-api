import re
import unicodedata
from typing import List, Dict

from pony.orm import db_session

from src.start import get_db
from src.models import GameTypeEnum

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


def create_game_bools(game, request):
    """Step 1: Create game properties with a simple True/False value.
    """
    game.exhausting = request['exhausting']
    game.touching = request['touching']
    game.scalable = request['scalable']
    game.digital = request['digital']


def create_game_categories(game, request):
    """Step 2: Create game properties that rely on Enums/Many-to-Many relationships.
    """
    for item in request['game_types']:
        game.game_types.add(db.GameType.get(slug=item))
    for item in request['game_lengths']:
        game.game_lengths.add(db.GameLength.get(slug=item))
    for item in request['group_sizes']:
        game.group_sizes.add(db.GroupSize.get(slug=item))

    if request.get('group_needs') is not None:
        for item in request['group_needs']:
            group_need = db.GroupNeed.get(slug=item['slug'])
            db.GroupNeedScore(game=game, group_need=group_need, value=item['score'])


def create_game_descriptive(game, request):
    """Step 3: Create game names and descriptions
    """
    for item in request['names']:
        slug = slugify(item)
        if db.Name.get(slug=slug):
            raise ValueError(f"A game with the name \"{slug}\" exists already.")
        game.names.create(slug=slug, full=item)

    for item in request['descriptions']:
        game.descriptions.create(text=item)


def create_game_materials(game, request):
    """Step 4: Create and link materials
    """
    if request.get('materials'):
        for item in request['materials']:
            slug = slugify(item)
            existing_item = db.Material.get(slug=slug)
            if existing_item:
                game.materials.add(existing_item)
            else:
                game.materials.create(slug=slug, full=item)


def create_game_prior_prep(game, request):
    """Step 5: Create prior preparation
    """
    if request.get('prior_prep'):
        game.prior_prep = request['prior_prep']


def create_game_meta(game: db.Game, request):
    """Step 6: Create game meta
    """
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
def create_games(games: List[Dict]):
    """Create one or several new games from the given list and save them in the database.
    """
    created_instances = []
    errors = []

    for game in games:
        try:
            game_license = create_game_license(game)
            new_instance = db.Game(license=game_license)
            create_game_bools(game=new_instance, request=game)
            create_game_categories(game=new_instance, request=game)
            create_game_descriptive(game=new_instance, request=game)
            create_game_materials(game=new_instance, request=game)
            create_game_prior_prep(game=new_instance, request=game)
            create_game_meta(game=new_instance, request=game)
        except ValueError as err:
            errors.append(err)
            new_instance.delete()
            continue
        created_instances.append(new_instance)

    return created_instances, errors


@db_session
def create_references(references):
    """Create one or several references from the given list of references and save them to the database.
    """
    created_instances = []
    errors = []

    for ref in references:
        try:
            name = db.Name.get(slug=ref['refers_to'])
            game = name.game
            if ref.get('url') and db.Reference.get(url=ref['url']):
                raise ValueError(f"Reference \"{ref['url']}\" exists already.")
            slug = name.slug + '-ref-' + str(len(game.references))
            new_instance = db.Reference(slug=slug, full=ref['full'], url=ref['url'])
            new_instance.games.add(game)
        except ValueError as err:
            errors.append(err)
            continue
        created_instances.append(new_instance.slug)

    return created_instances, errors


@db_session
def create_collections(collections):
    """Create or attach to one or several collections from the given list of CollectionIn.
    """
    used_instances = []
    errors = []

    for collection in collections:
        try:
            if collection.slug:
                slug = collection.slug
            else:
                slug = slugify(collection.full)

            instance = db.Collection.get(slug=slug)
            if not instance:
                instance = db.Collection(slug=slug, full=collection.full)
            used_instances.append(instance)

            for game in collection.games:
                instance.games.add(game)
        except ValueError as err:
            errors.append(err)
            continue
        used_instances.append(instance.slug)

    return used_instances, errors

