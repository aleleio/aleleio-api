from datetime import datetime

from pony.orm import *


def define_entities_meta(db):

    class GameMeta(db.Entity):
        game = Required(lambda: db.Game)

        timestamp = Required(datetime, default=datetime.utcnow)
        author_id = Required(int)

    class License(db.Entity):
        games = Set(lambda: db.Game)

        name = Required(str, default="CC BY-SA 4.0")
        url = Optional(str, default="https://creativecommons.org/licenses/by-sa/4.0/")
        owner = Optional(str, default="alele.io")
        owner_url = Optional(str, default="https://alele.io")

    class Reference(db.Entity):
        game = Required(lambda: db.Game)

        timestamp = Required(datetime, default=datetime.utcnow)
        slug = Required(str)
        full = Required(str)
        url = Optional(str, unique=True)

    class Collection(db.Entity):
        games = Set(lambda: db.Game)

        author_id = Required(int)
        slug = Required(str, unique=True)
        full = Required(str)
        description = Optional(LongStr)

