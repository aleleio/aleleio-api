from flask import Blueprint
from pony.orm import *

from src.services.import_to_db import run_import
from src.start import get_project_version, get_db

db = get_db()


@db_session
def about():
    return {"version": get_project_version(),
            "games": len(db.Game.select())}


def start_import():
    delete_all()
    return run_import()


@db_session
def delete_all():
    """Bulk delete in separate db_session, otherwise remnants remain
    """
    db.Game.select().delete(bulk=True)
