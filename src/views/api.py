from pony.orm import *

from src.services.import_to_db import run_import
from src.start import get_project_version, get_db

db = get_db()


@db_session
def about():
    return {
        "api": {
            "version": get_project_version(),
            "last_commit": "n/a",
            "last_import": "n/a",
            "url": "https://github.com/aleleio/aleleio-api",
        },
        "web": {
            "version": "0.5.1 from CHANGES.md",
            "last_commit": "n/a",
            "url": "https://github.com/aleleio/aleleio-web",
        },
        "tb_repo": {
            "last_commit": "n/a",
            "games": len(db.Game.select()),
            "references": "n/a",
            "url": "https://github.com/aleleio/teambuilding-games",
        }
    }


def start_import():
    delete_all()
    return run_import()


@db_session
def delete_all():
    """Bulk delete in separate db_session, otherwise remnants remain
    """
    db.Game.select().delete(bulk=True)
