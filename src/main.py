from functools import lru_cache
from pathlib import Path

import fastapi

from starlette.staticfiles import StaticFiles
from fastapi import Depends
from pony.orm import set_sql_debug

from src.config import Settings
from src.models import db_games, db_users

api = fastapi.FastAPI()


@lru_cache
def get_settings():
    """Load pydantic Settings object in a dependency
    https://fastapi.tiangolo.com/advanced/settings/#settings-in-a-dependency
    Todo: Maybe this could be simplified if Settings Override for Testing is not actually needed
    """
    return Settings


def configure():
    """Configure the application
    Get settings with os.getenv() and use settings object in the future
    ToDo: https://fastapi.tiangolo.com/advanced/settings/#pydantic-settings
    """
    init_database()
    configure_routing()


def init_database(settings: Settings = Depends(get_settings())):
    db_games.bind(provider='sqlite', filename='db_games.sqlite', create_db=True)
    # db_games.bind(provider='mysql', host='', user='', passwd='', db='')
    db_games.generate_mapping(create_tables=True)

    db_users.bind(provider='sqlite', filename='db_users.sqlite', create_db=True)
    # db_users.bind(provider='mysql', host='', user='', passwd='', db='')
    db_users.generate_mapping(create_tables=True)

    set_sql_debug(True)


def configure_routing():
    """Set all routes
    FastAPI's routers are similar to Flask Blueprints
    """
    project_root = Path(__file__).parent.parent
    static_path = project_root.joinpath('src', 'static')
    api.mount('/static', StaticFiles(directory=static_path), name='static')

    from src.views import games, terms, meta, home
    api.include_router(home.router)
    api.include_router(games.router)
    api.include_router(terms.router)
    api.include_router(meta.router)
