from pony.orm import *

from src.services.connect_github import get_latest_commit
from src.services.import_to_db import run_import
from src.start import get_db

db = get_db()


@db_session
def about():
    api = db.APIInfo.get(name="aleleio-api").to_dict(exclude=["id", "games", "references"])
    web = db.APIInfo.get(name="aleleio-web").to_dict(exclude=["id", "games", "references", "last_import"])
    tb = db.APIInfo.get(name="teambuilding-games").to_dict(exclude=["id", "last_import"])
    return {"api": {**api}, "web": {**web}, "teambuilding-games": {**tb}}


def start_import():
    delete_all()
    return run_import()


@db_session
def check_do_import(repo):
    """Github Actions hook to start updates.
    """
    timestamp = get_latest_commit(repo["name"])
    entry = db.APIInfo.get(name=repo["name"])
    entry.last_commit = timestamp


@db_session
def delete_all():
    """Bulk delete in separate db_session, otherwise remnants remain
    """
    db.Game.select().delete(bulk=True)
