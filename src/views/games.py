import fastapi
from fastapi import Depends

from src.models import GameQuery

router = fastapi.APIRouter()


@router.get('/games')
def all_games_view(query: GameQuery = Depends()):
    # http GET http://localhost:8000/games group_needs:='{"main": "name"}'
    limit = query.limit
    if query.basic:
        return {
            "game_type": query.basic.game_type,
            "group_size": query.basic.group_size,
            "game_length": query.basic.game_length,
        }
    elif query.group_needs:
        return {
            "main": query.group_needs.main,
            "aux1": query.group_needs.aux1,
            "aux2": query.group_needs.aux2,
        }
    else:
        return {"result": "all games"}


@router.get('/games/{game_id}')
def single_game_view(game_id):
    pass


@router.post('/games')
def create_game_view():
    pass


@router.patch('/games/{game_id}')
def update_game_view(game_id):
    pass


@router.delete('/games/{game_id}')
def delete_game_view(game_id):
    pass
