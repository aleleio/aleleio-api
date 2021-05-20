import re
import unicodedata
from typing import List

from pony.orm import db_session

from src.models import Game, GameIn, GameType, GameLength, GroupSize, GroupNeedScore, GroupNeed, \
    Name, Material, GameMeta, License, ReferenceIn, Reference, CollectionIn, Collection


def slugify(value):
    """Django's slugify - Create an ascii string from unicode
    Convert spaces or repeated dashes to single dashes. Remove characters that aren't alphanumerics, underscores,
    or hyphens. Convert to lowercase. Also strip leading and trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')


def create_game_bools(game: Game, request: GameIn):
    """Step 1: Create Game properties with a simple True/False value.
    """
    request_bools = {
        'exhausting': request.exhausting,
        'touching': request.touching,
        'scalable': request.scalable,
        'digital': request.digital,
    }
    game.set(**request_bools)


def create_game_relationships(game: Game, request: GameIn):
    """Step 2: Create Game properties that rely on Enums/Many-to-Many relationships.
    """
    for item in request.game_types:
        game.game_types.add(GameType.get(slug=item))
    for item in request.game_lengths:
        game.game_lengths.add(GameLength.get(slug=item))
    for item in request.group_sizes:
        game.group_sizes.add(GroupSize.get(slug=item))
    for item in request.group_needs:
        group_need = GroupNeed.get(slug=item.slug)
        GroupNeedScore(game=game, group_need=group_need, value=item.score)


def create_game_unique(game: Game, request: GameIn):
    """Step 3: Create Game properties that don't fit into other categories.
    """
    for item in request.names:
        slug = slugify(item)
        if Name.get(slug=slug):
            raise ValueError(f"A game with the name \"{slug}\" exists already.")
        game.names.create(slug=slug, full=item)
    for item in request.descriptions:
        game.descriptions.create(text=item)
    for item in request.materials:
        slug = slugify(item)
        found_item = Material.get(slug=slug)
        if found_item:
            game.materials.add(found_item)
        else:
            game.materials.create(slug=slug, full=item)
    if request.prior_prep is not None:
        game.prior_prep = request.prior_prep


def create_game_meta(game: Game, request: GameIn):
    """
    """
    GameMeta(
        game=game,
        author_id=1,  # Todo: Validation with actual User!
    )


@db_session
def create_games(games: List[GameIn]):
    """Create one or several new games from the given list of GameIn and save them in the database.
    """
    created_instances = []
    errors = []

    for game in games:
        try:
            new_instance = Game(license=License(**game.license.dict()))
            create_game_bools(game=new_instance, request=game)
            create_game_relationships(game=new_instance, request=game)
            create_game_unique(game=new_instance, request=game)
            create_game_meta(game=new_instance, request=game)
        except ValueError as err:
            errors.append(err)
            new_instance.delete()
            continue
        created_instances.append(new_instance.id)

    return created_instances, errors


@db_session
def create_references(references: List[ReferenceIn]):
    """
    """
    created_instances = []
    errors = []

    for ref in references:
        try:
            name = Name.get(lambda n: ref.game_slug in n.slug)
            game = name.game
            slug = name.slug + '-ref-' + str(len(game.references))
            # Todo: Check for duplicates
            new_instance = Reference(slug=slug, full=ref.full, url=ref.url)
            new_instance.games.add(game)
        except ValueError as err:
            errors.append(err)
            new_instance.delete()
            continue
        created_instances.append(new_instance.slug)

    return created_instances, errors


@db_session
def create_collections(collections: List[CollectionIn]):
    """
    """
    used_instances = []
    errors = []

    for collection in collections:
        try:
            if collection.slug:
                slug = collection.slug
            else:
                slug = slugify(collection.full)

            instance = Collection.get(slug=slug)
            if not instance:
                instance = Collection(slug=slug, full=collection.full)
            used_instances.append(instance)

            for game in collection.games:
                instance.games.add(game)
        except ValueError as err:
            errors.append(err)
            continue
        used_instances.append(instance.slug)

    return used_instances, errors

