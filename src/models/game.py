"""
SQL
"""

from pony.orm import *

db_games = Database()


class Game(db_games.Entity):
    names = Set(lambda: Name)
    descriptions = Set(lambda: Description)
    materials = Set(lambda: Material)
    game_types = Set(lambda: GameType)
    game_lengths = Set(lambda: GameLength)
    group_sizes = Set(lambda: GroupSize)
    group_need_scores = Set(lambda: GroupNeedScore)

    meta = Optional(lambda: db_games.GameMeta, cascade_delete=True)
    sources = Set(lambda: db_games.Source)
    collections = Set(lambda: db_games.Collection)
    versions = Set(lambda: db_games.Version)

    statistic = Optional(lambda: db_games.GameStatistic, cascade_delete=True)


    prior_prep = Optional(LongStr)
    exhausting = Optional(bool)
    touching = Optional(bool)
    scalable = Optional(bool)
    digital = Optional(bool)


class Name(db_games.Entity):
    game = Required(Game)

    slug = Required(str)
    full = Required(str)


class Description(db_games.Entity):
    game = Required(Game)

    text = Required(LongStr)


class Material(db_games.Entity):
    games = Set(Game)

    slug = Required(str)
    full = Required(str)


class GameType(db_games.Entity):
    games = Set(Game)

    slug = Required(str)
    full = Required(str)


class GameLength(db_games.Entity):
    games = Set(Game)

    slug = Required(str)
    full = Required(str)


class GroupSize(db_games.Entity):
    games = Set(Game)

    slug = Required(str)
    full = Required(str)


class GroupNeed(db_games.Entity):
    scores = Set(lambda: GroupNeedScore)

    slug = Required(str)
    full = Required(str)


class GroupNeedScore(db_games.Entity):
    game = Required(Game)
    group_need = Required(GroupNeed)
    PrimaryKey(game, group_need)

    value = Required(int, default=0)
