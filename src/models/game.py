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
        exhausting = Optional(bool, default=False)
        touching = Optional(bool, default=False)
        scalable = Optional(bool, default=False)
        digital = Optional(bool, default=False)

        def to_schema_out(self):
            """Build a JSON-serialisable dict that is validated as GameOut
            """
            result = self.to_dict(only=['id', 'prior_prep', 'exhausting', 'touching', 'scalable', 'digital'], with_lazy=True)
            result['names'] = [n.to_dict(exclude='game') for n in self.names]
            result['descriptions'] = [obj.to_dict(exclude='game', with_lazy=True) for obj in self.descriptions]
            result['game_types'] = [obj.to_dict() for obj in self.game_types]
            result['game_lengths'] = [obj.to_dict() for obj in self.game_lengths]
            result['group_sizes'] = [obj.to_dict() for obj in self.group_sizes]
            result['group_needs'] = [obj.to_dict(exclude='game', related_objects=True) for obj in self.group_need_scores]
            for item in result['group_needs']:
                item['need'] = item['group_need'].slug
                del item['group_need']
            result['materials'] = [obj.to_dict(exclude=['games']) for obj in self.materials]
            result['license'] = self.license.to_dict()
            result['meta'] = self.meta.to_dict(exclude=['id', 'game'])
            return result

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
