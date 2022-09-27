from flask import Blueprint
from pony.orm import *

from src.services.authentication import auth_required
from src.services.import_to_db import run_import
from src.start import get_project_version, get_db

db = get_db()
bp = Blueprint('api', __name__)


@db_session
def about():
    return {"version": get_project_version(),
            "games": len(db.Game.select())}


@bp.route('/import')
@auth_required
def start_import():
    try:
        run_import()
    except CacheIndexError as err:
        return {"error": err}
    return {"result": 200}
