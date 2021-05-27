"""
Routes for all /game and /games related operations

"""
from typing import List

import fastapi
from fastapi import Depends
from pony.orm import db_session

from src.models import GameQuery, GameOut, GameIn, Game, GameORM
from src.services import search, create, update

router = fastapi.APIRouter()


@router.get('/games', tags=['games'], response_model=List[GameOut])
def all_games_view(query: GameQuery = Depends(GameQuery)):
    result = search.all_games(query)
    # statistics.get_all_games(user, query, result)
    # log(user, query, result)
    return result


@router.get('/games/{game_id}', tags=['games'], response_model=GameOut)
@db_session
def single_game_view(game_id: int):
    # Todo: Also allow for slug as game_id?
    result = GameORM.from_orm(Game[game_id])
    return result


@router.post('/games', tags=['games'])
def create_games_view(request_objects: List[GameIn]):
    result, errors = create.create_games(request_objects)
    # statistics.post_create_game(user, request, result)
    # log(user, request, result)
    return result


@router.patch('/games/{game_id}', tags=['games'])
def update_game_view(game_id, game=GameIn):
    result = update.single_game(game_id, game=game)


@router.delete('/games/{game_id}', tags=['games'])
def delete_game_view(game_id):
    pass
