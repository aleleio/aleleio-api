"""
Routes for all /game and /games related operations

"""
from typing import List

import fastapi
from fastapi import Depends

from src.models import GameQuery, PostRequestGame
from src.services import searching
from src.services.create import create_game

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
def create_game_view(request_objects: List[PostRequestGame]):
    result = create_game(request_objects)
    # statistics.post_create_game(user, request, result)
    # log(user, request, result)
    return result


@router.patch('/games/{game_id}', tags=['games'])
def update_game_view(game_id):
    pass


@router.delete('/games/{game_id}', tags=['games'])
def delete_game_view(game_id):
    pass
