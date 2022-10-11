import datetime
import itertools
import json
import os
from functools import cache
from pathlib import Path

from connexion import FlaskApp
from connexion.resolver import RelativeResolver
from dotenv import load_dotenv
from flask import request
from flask_cors import CORS
from pony.orm import Database, set_sql_debug, db_session

from src.models import define_entities_game, define_entities_meta, define_entities_user, GameTypeEnum, GameLengthEnum, \
    GroupSizeEnum, GroupNeedEnum, define_entities_stats, define_entities_api
from src.services.enforcedefaults import validator_remap

# Load project root and constants from dotenv file
ROOT = Path(__file__).parent.parent
dotenv_path = ROOT.joinpath('.env')
load_dotenv(dotenv_path)


@cache
def get_db(users_db=False):
    """Bind Pony ORM to database
    This acts like a singleton because of caching.
    """
    if users_db:
        credentials = json.loads(os.environ.get("DB_USERS_CONNECT"))
    else:
        credentials = json.loads(os.environ.get("DB_CONNECT"))

    if not os.environ.get("FLASK_DEBUG"):  # pragma: no cover / production
        database = Database(provider='mysql', **credentials)
    elif os.environ.get('FLASK_TESTING'):
        # database = Database(provider='sqlite', filename=f'testing_{credentials["db"]}.sqlite', create_db=True)
        database = Database(provider='sqlite', filename=f':memory:', create_db=True)
    else:  # pragma: no cover / development
        database = Database(provider='sqlite', filename=f'{credentials["db"]}.sqlite', create_db=True)

    if users_db:
        define_entities_user(database)
    else:
        define_entities_game(database)
        define_entities_meta(database)
        define_entities_stats(database)
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
    CORS(connexion_app.app)
    connexion_app.add_api(
        'openapi.yml',
        resolver=RelativeResolver('src.views'),
        validate_responses=True,
        validator_map=validator_remap,
    )
    connexion_app.app.config.from_prefixed_env()

    @connexion_app.app.after_request
    @db_session
    def activity_tracking(response):
        from src.services import tracking
        if response.status_code in [200, 201]:
            session = tracking.get_session(request)
            tracking.add_request(session, request, response)
        return response

    return connexion_app


@db_session
def run_startup_tasks(db):  # pragma: no cover
    if hasattr(db, 'User'):
        if db.User.get(login="admin"):
            return
        startup_users_db(db)
    else:
        if db.APIInfo.get(name="aleleio-api"):
            return
        startup_api_info(db)
        startup_games_db(db)


def startup_users_db(udb):  # pragma: no cover
    for user in [os.environ.get("USER_ADMIN"), os.environ.get("USER_WEB"), os.environ.get("USER_ANDROID"), os.environ.get("USER_IOS")]:
        udb.User(**json.loads(user))


def startup_games_db(db):
    """Seed database with category enums if not already present
    """
    for item in GameTypeEnum:
        db.GameType(slug=item.value, full=item.full)
    for item in GameLengthEnum:
        db.GameLength(slug=item.value, full=item.full)
    for item in GroupSizeEnum:
        db.GroupSize(slug=item.value, full=item.full)
    for item in GroupNeedEnum:
        db.GroupNeed(slug=item.value, full=item.full)

    for item in itertools.chain(GameTypeEnum, GameLengthEnum, GroupSizeEnum, GroupNeedEnum):
        db.QueryParam(slug=item.value)


def startup_api_info(db):
    from src.services.api_info import get_project_version
    from src.services.connect_github import get_latest_commit

    for project in ["aleleio-api", "teambuilding-games"]:
        params = dict(
            name=project,
            version=get_project_version(project),
            last_commit=get_latest_commit(project),
            url=f"https://github.com/aleleio/{project}"
        )
        db.APIInfo(**params)

    for project in ["aleleio-web"]:
        params = dict(
            name=project,
            version=get_project_version(project),
            last_commit=datetime.datetime.utcnow(),
            url=f"https://github.com/aleleio/{project}"
        )
        db.APIInfo(**params)
