from datetime import datetime

from pony.orm import *


def define_entities_stats(db):
    class Session(db.Entity):
        queries = Set(lambda: Query)

        user_id = Required(int)
        origin = Optional(str)  # web, android, ios
        starttime = Required(datetime, default=datetime.utcnow)
        endtime = Required(datetime, default=datetime.utcnow)  # update on every route
        user_agent = Required(str)
        remote_addr = Required(str)

    class Query(db.Entity):
        """API query statistics
        """
        session = Required(Session)
        params = Set(lambda: QueryParam)

        timestamp = Required(datetime, default=datetime.utcnow)
        path = Required(str)
        query_type = Required(str)  # basic / group_needs
        game_id = Optional(int)
        result_length = Optional(int)

    class QueryParam(db.Entity):
        """API query parameters
        """
        query = Required(Query)
        slug = Required(str)

    class GameStatistic(db.Entity):
        """Search statistics for each individual game.
        """
        game = Required(lambda: db.Game)

        search_impressions = Optional(int)
        detail_impressions = Optional(int)
        last_impression = Optional(datetime)
