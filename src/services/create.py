import re
import unicodedata
from typing import List

from pony.orm import db_session

from src.models import Game, GameMeta, PostRequestGame, GameType, GameLength, GroupSize, GroupNeedScore, GroupNeed, \
    Name, Material


def slugify(value):
    """Django's slugify - Create an ascii string from unicode
    Convert spaces or repeated dashes to single dashes. Remove characters that aren't alphanumerics, underscores,
    or hyphens. Convert to lowercase. Also strip leading and trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')


def create_game_bools(game: Game, request: PostRequestGame):
    """Step 1: Create Game properties with a simple True/False value.
    """
    request_bools = {
        'exhausting': request.exhausting,
        'touching': request.touching,
        'scalable': request.scalable,
        'digital': request.digital,
    }
    game.set(**request_bools)


def create_game_relationships(game: Game, request: PostRequestGame):
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


def create_game_unique(game: Game, request: PostRequestGame):
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


@db_session
def create_game(request_objects: List[PostRequestGame]):
    """Create one or several new games from the given list of PostRequestGame and save them in the database.
    """
    created_games = []

    for request in request_objects:
        new_game = Game()
        create_game_bools(game=new_game, request=request)
        create_game_relationships(game=new_game, request=request)
        create_game_unique(game=new_game, request=request)
        created_games.append(new_game.id)

        # GameMeta(game=new_game, author_id=user.id)

    return created_games