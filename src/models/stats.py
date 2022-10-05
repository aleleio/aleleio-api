from datetime import datetime

from pony.orm import *


def define_entities_stats(db):
    class Session(db.Entity):
        requests = Set(lambda: Request)

        user_id = Required(int)
        origin = Optional(str)  # web, android, ios
        starttime = Required(datetime, default=datetime.utcnow)
        endtime = Required(datetime, default=datetime.utcnow)  # update on every route
        user_agent = Required(str)
        remote_addr = Required(str)

    class Request(db.Entity):
        """API query statistics
        """
        session = Required(Session)
        query_params = Set(lambda: QueryParam)

        query_type = Optional(str)  # basic / group_needs
        timestamp = Required(datetime, default=datetime.utcnow)
        path = Required(str)
        method = Required(str)
        game_id = Optional(int)
        result_length = Optional(int)

    class QueryParam(db.Entity):
        """API query parameters
        """
        request = Required(Request)
        slug = Required(str)

    class GameStatistic(db.Entity):
        """Search statistics for each individual game.
        """
        game = Required(lambda: db.Game)

        search_impressions = Optional(int)
        detail_impressions = Optional(int)
        last_impression = Optional(datetime)
