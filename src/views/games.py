"""
Routes for all /game and /games related operations

"""
import fastapi
from fastapi import Depends

from src.models import GameQuery
from src.services import searching

router = fastapi.APIRouter()


@router.get('/games', tags=['games'])
def all_games_view(query: GameQuery = Depends(GameQuery)):
    result = searching.all_games(query)
    # statistics.get_all_games(user, query, result)
    # log(user, query, result)
    return result


@router.get('/games/{game_id}', tags=['games'])
def single_game_view(game_id: int):
    pass


@router.post('/games', tags=['games'])
def create_game_view():
    pass


@router.patch('/games/{game_id}', tags=['games'])
def update_game_view(game_id):
    pass


@router.delete('/games/{game_id}', tags=['games'])
def delete_game_view(game_id):
    pass
