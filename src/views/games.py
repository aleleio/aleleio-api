import fastapi
from fastapi import Depends

from src.models import GameQuery

router = fastapi.APIRouter()


@router.get('/games', tags=['games'])
def all_games_view(query: GameQuery = Depends()):
    # http GET http://localhost:8000/games group_needs:='{"main": "name"}'
    return {"result": "all games"}


@router.get('/games/{game_id}', tags=['games'])
def single_game_view(game_id):
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
