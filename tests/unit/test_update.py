import pytest

from pony.orm import db_session

from src.services.search import all_games
from src.services.create import create_games
from src.services.update import update_game

GAMEA = {'names': ['A'], 'descriptions': ['A'],
         'game_types': ['ice'], 'game_lengths': ['short'], 'group_sizes': ['small'],
         'exhausting': False, 'touching': False, 'scalable': False, 'digital': False}
GAMEB = {'names': ['B'], 'descriptions': ['B'],
         'game_types': ['song'], 'game_lengths': ['medium'], 'group_sizes': ['large'],
         'exhausting': False, 'touching': False, 'scalable': False, 'digital': False}
GAMEC = {'names': ['C'], 'descriptions': ['C'],
         'game_types': ['gtk'], 'game_lengths': ['long'], 'group_sizes': ['multiple'],
         'exhausting': False, 'touching': False, 'scalable': False, 'digital': False}


@pytest.fixture()
def populate(db):
    create_games([GAMEA, GAMEB, GAMEC])


@db_session
def test_update_game(db, populate):
    game = db.Game.get(id=1)
    n1 = db.Name.get(slug='a')
    gt1 = db.GameType.get(slug='ice')
    gt2 = db.GameType.get(slug="song")
    gt3 = db.GameType.get(slug='race')
    gl1 = db.GameLength.get(slug='short')
    assert n1 in game.names
    assert gt1 in game.game_types
    assert gl1 in game.game_lengths

    request = {"game_types": []}
    result, _ = update_game(game, request)
    assert gt1 not in result.game_types
    assert len(result.game_types) == 0

    request = {"game_types": ["song"]}
    result, _ = update_game(game, request)
    assert gt2 in result.game_types
    assert len(result.game_types) == 1

    request = {"game_types": ["race", "ice"]}
    result, _ = update_game(game, request)
    assert gt1 in result.game_types
    assert gt3 in result.game_types
    assert len(result.game_types) == 2
