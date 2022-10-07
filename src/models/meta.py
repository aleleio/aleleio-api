from datetime import datetime

from pony.orm import *


def define_entities_meta(db):

    class GameMeta(db.Entity):
        timestamp = Required(datetime, default=datetime.utcnow)
        game_id = Required(int, unique=True)
        author_id = Required(int)

    class License(db.Entity):
        games = Set(lambda: db.Game)

        name = Required(str, default="CC BY-SA 4.0")
        url = Optional(str, default="https://creativecommons.org/licenses/by-sa/4.0/")
        owner = Optional(str, default="alele.io")
        owner_url = Optional(str, default="https://alele.io")

    class Reference(db.Entity):
        timestamp = Required(datetime, default=datetime.utcnow)
        game_id = Required(int)
        slug = Required(str, unique=True)
        full = Required(str)
        url = Required(str, unique=True)

    class Collection(db.Entity):
        games = Set(lambda: db.Game)

        author_id = Required(int)
        slug = Required(str, unique=True)
        full = Required(str)
        description = Optional(LongStr)

