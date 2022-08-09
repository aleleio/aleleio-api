"""
SQL
"""

from pony.orm import *


def define_entities_game(db):

    class Game(db.Entity):
        names = Set(lambda: Name)
        descriptions = Set(lambda: Description)
        materials = Set(lambda: Material)
        game_types = Set(lambda: GameType)
        game_lengths = Set(lambda: GameLength)
        group_sizes = Set(lambda: GroupSize)
        group_need_scores = Set(lambda: GroupNeedScore)

        meta = Optional(lambda: db.GameMeta, cascade_delete=True)
        license = Required(lambda: db.License)
        references = Set(lambda: db.Reference)
        collections = Set(lambda: db.Collection)
        versions = Set(lambda: db.Version)

        statistic = Optional(lambda: db.GameStatistic, cascade_delete=True)

        prior_prep = Optional(LongStr)
        exhausting = Optional(bool)
        touching = Optional(bool)
        scalable = Optional(bool)
        digital = Optional(bool)

    class Name(db.Entity):
        game = Required(Game)

        slug = Required(str)
        full = Required(str)

    class Description(db.Entity):
        game = Required(Game)

        text = Required(LongStr)

    class Material(db.Entity):
        games = Set(Game)

        slug = Required(str)
        full = Required(str)

    class GameType(db.Entity):
        games = Set(Game)

        slug = Required(str)
        full = Required(str)

    class GameLength(db.Entity):
        games = Set(Game)

        slug = Required(str)
        full = Required(str)

    class GroupSize(db.Entity):
        games = Set(Game)

        slug = Required(str)
        full = Required(str)

    class GroupNeed(db.Entity):
        scores = Set(lambda: GroupNeedScore)

        slug = Required(str)
        full = Required(str)

    class GroupNeedScore(db.Entity):
        game = Required(Game)
        group_need = Required(GroupNeed)
        PrimaryKey(game, group_need)

        value = Required(int, default=0)
