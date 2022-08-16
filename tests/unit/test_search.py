import pytest
from pony.orm import db_session

from src.services.search import all_games
from src.services.create import create_games

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
@db_session()
def populate_with_abc(db):
    create_games([GAMEA, GAMEB, GAMEC])


def test_all_games_gt(db, populate_with_abc):
    query = {"game_type": "ice"}
    result = all_games(query)
    assert len(result) == 1
    assert result[0]['names'][0]['full'] == 'A'


def test_all_games_gl(db, populate_with_abc):
    query = {"game_length": "medium"}
    result = all_games(query)
    assert len(result) == 1
    assert result[0]['names'][0]['full'] == 'B'


def test_all_games_gs(db, populate_with_abc):
    query = {"group_size": "multiple"}
    result = all_games(query)
    assert len(result) == 1
    assert result[0]['names'][0]['full'] == 'C'


def test_all_games_gn():
