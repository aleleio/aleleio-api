"""
Routes for all /game and /games related operations

"""
from typing import List

import fastapi
from fastapi import Depends

from src.models import GameQuery, GameOut, GameIn
from src.services import search, read
from src.services.create import create_games

router = fastapi.APIRouter()


@router.get('/games', tags=['games'], response_model=List[GameOut])
def all_games_view(query: GameQuery = Depends(GameQuery)):
    result = search.all_games(query)
    # statistics.get_all_games(user, query, result)
    # log(user, query, result)
    return result


@router.get('/games/{game_id}', tags=['games'], response_model=GameOut)
def single_game_view(game_id: int):
    result = read.single_game(game_id)
    return result


@router.post('/games', tags=['games'])
def create_games_view(request_objects: List[GameIn]):
    result, errors = create_games(request_objects)
    # statistics.post_create_game(user, request, result)
    # log(user, request, result)
    return result


@router.patch('/games/{game_id}', tags=['games'])
def update_game_view(game_id):
    pass


@router.delete('/games/{game_id}', tags=['games'])
def delete_game_view(game_id):
    pass
