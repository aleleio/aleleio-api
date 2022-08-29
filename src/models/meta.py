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

    class Version(db.Entity):
        game = Required(lambda: db.Game)
        changesets = Set(lambda: VersionChangeset)

        author_id = Required(int)
        timestamp = Required(datetime, default=datetime.utcnow)

    class VersionChangeset(db.Entity):
        """For each changed entity in a new version of a game,
        track the detailed changes and store them in a VersionChangeset
        (e.g. one changeset for key="name"; an additional name)
        """
        version = Required(Version)

        key = Required(str)
        value = Required(LongStr)
        key_id = Optional(int)
        score = Optional(int)
        url = Optional(str)
        action = Required(str)

    class GameStatistic(db.Entity):
        """Search statistics for each individual game.
        New in 0.6: Directly link the queries in which a game appeared
        """
        game = Required(lambda: db.Game)
        queries = Set(lambda: QueryStatistic)

        search_impressions = Optional(int)
        detail_impressions = Optional(int)
        last_impression = Optional(datetime)

    class QueryStatistic(db.Entity):
        """API query statistics
        """
        game_statistics = Set(GameStatistic)

        timestamp = Required(datetime, default=datetime.utcnow)
        user_id = Required(int)
        request_origin = Required(str)
        request_uri = Required(str)
        request_type = Required(str)
        request_game_id = Optional(int)
        request_param = Optional(lambda: QueryStatisticParam)
        request_result = Optional(int)

    class QueryStatisticParam(db.Entity):
        """API query parameters
        New in 0.6: Add group_needs tracking
        """
        query = Required(QueryStatistic)

        query_type = Optional(str)  # basic / group_needs
        game_type = Optional(str)
        game_length = Optional(str)
        group_size = Optional(str)
        main = Optional(str)
        aux1 = Optional(str)
        aux2 = Optional(str)
        limit = Optional(int)
