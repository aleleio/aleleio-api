from pony.orm import db_session

from src.main import database as db
from src.models import GameIn, GameOut


@db_session
def update_game(game_id: int, game: GameIn):
    stored_game_data = db.Game[game_id]
    stored_game_model = GameOut
