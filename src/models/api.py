from datetime import datetime

from pony.orm import *


def define_entities_api(db):
    class APIInfo(db.Entity):
        name = Required(str, unique=True)
        version = Required(str)
        last_commit = Required(datetime)
        url = Required(str, default="https://github.com/aleleio")

        # API
        last_import = Optional(datetime)

        # Web

        # Teambuilding-Games
        games = Optional(int)
        references = Optional(int)
