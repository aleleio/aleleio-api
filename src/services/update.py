from pony.orm import db_session

from src.models import GameIn, Game, GameOut


@db_session
def update_game(game_id: int, game: GameIn):
    stored_game_data = Game[game_id]
    stored_game_model = GameOut
