import json
import os
from functools import cache
from pathlib import Path

import yaml
from connexion import FlaskApp
from connexion.resolver import RelativeResolver
from dotenv import load_dotenv
from pony.orm import Database, set_sql_debug, db_session

from src.models import define_entities_game, define_entities_meta, define_entities_user, GameTypeEnum, GameLengthEnum, \
    GroupSizeEnum, GroupNeedEnum, define_entities_api, UserRoleEnum, UserStatusEnum
from src.services.enforcedefaults import validator_remap

# Define project root and load constants from dotenv file
ROOT = Path(__file__).parent.parent
dotenv_path = ROOT.joinpath('.env')
load_dotenv(dotenv_path)


@cache
def get_project_version():
    """Get the current version from openapi.yml config file.
    """
    yml_path = ROOT.joinpath('openapi.yml')
    with open(yml_path, 'r') as fin:
        yml = yaml.safe_load(fin)

    return yml['info']['version']


@cache
def get_db(users_db=False):
    """Bind Pony ORM to database
    This acts like a singleton because of caching.
    """

    if users_db:
        credentials = json.loads(os.environ.get("DB_USERS_CONNECT"))
    else:
        credentials = json.loads(os.environ.get("DB_CONNECT"))

    if not os.environ.get("FLASK_DEBUG"):  # production
        database = Database(provider='mysql', **credentials)
    elif os.environ.get('FLASK_TESTING'):
        database = Database(provider='sqlite', filename=f'testing_{credentials["db"]}.sqlite', create_db=True)
    else:  # development
        database = Database(provider='sqlite', filename=f'{credentials["db"]}.sqlite', create_db=True)

    if users_db:
        define_entities_user(database)
    else:
        define_entities_game(database)
        define_entities_meta(database)
        define_entities_api(database)

    database.generate_mapping(create_tables=True)
    set_sql_debug(False)
    return database


@cache
def get_app():
    """Connexion Wrapper App
    Connexion creates a wrapper around a Flask app, through which all requests are passed.
    The Connexion wrapper app is called by wsgi.py and pytest.
    You can access the Flask app with `app.app.properties`.
    """

    # Todo: Sentry integration
    # sentry_sdk.init(
    #     dsn=os.environ.get('SENTRY_DSN'),
    #     integrations=[FlaskIntegration()],
    #     # Reduce this for production, maybe 0.25
    #     traces_sample_rate=0.25,
    #     release=get_project_version(),
    #     environment=Config().SENTRY
    # )

    swagger_options = {
        'swagger_url': '/',
        'swagger_ui_config': {
            'operationsSorter': 'method',
            'tagsSorter': 'alpha',
        }
    }
    connexion_app = FlaskApp(__name__, specification_dir=ROOT, options=swagger_options)
    connexion_app.add_api(
        'openapi.yml',
        resolver=RelativeResolver('src.views'),
        validate_responses=True,
        validator_map=validator_remap,
    )
    connexion_app.app.config.from_prefixed_env()

    from src.views.api import bp
    connexion_app.app.register_blueprint(bp)

    return connexion_app


@db_session
def run_startup_tasks(db):
    """Seed database with category enums if not already present
    """
    if hasattr(db, 'User'):
        if not db.User.get(login="admin"):
            for user in [json.loads(os.environ.get("USER_ADMIN")), json.loads(os.environ.get("USER_WEB"))]:
                db.User(**user)

    else:
        if not db.GameType.get(slug="ice"):
            for item in GameTypeEnum:
                db.GameType(slug=item.value, full=item.full)
            for item in GameLengthEnum:
                db.GameLength(slug=item.value, full=item.full)
            for item in GroupSizeEnum:
                db.GroupSize(slug=item.value, full=item.full)
            for item in GroupNeedEnum:
                db.GroupNeed(slug=item.value, full=item.full)
