from pathlib import Path

import fastapi

from starlette.staticfiles import StaticFiles
from pony.orm import set_sql_debug

from src.config import Settings
from src.models import db_games, db_users


project_root = Path(__file__).parent.parent
env_path = project_root.joinpath('.env')

settings = Settings(_env_file=env_path)
api = fastapi.FastAPI()


def configure():
    """Configure the application
    Get settings with os.getenv() and use settings object in the future
    ToDo: https://fastapi.tiangolo.com/advanced/settings/#pydantic-settings
    """
    init_database()
    configure_routing()


def init_database():
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
    static_path = project_root.joinpath('src', 'static')
    api.mount('/static', StaticFiles(directory=static_path), name='static')

    from src.views import games, terms, meta, home
    api.include_router(home.router)
    api.include_router(games.router)
    api.include_router(terms.router)
    api.include_router(meta.router)
