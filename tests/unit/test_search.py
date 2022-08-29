import pytest

from src.services.search import all_games, all_names
from src.services.create import create_games

GAMEA = {'names': ['A'], 'descriptions': ['A'],
         'game_types': ['ice'], 'game_lengths': ['short'], 'group_sizes': ['small'],
         'group_needs': [{'slug': 'groupid', 'score': 3}, {'slug': 'energy', 'score': 5}],
         'exhausting': False, 'touching': False, 'scalable': False, 'digital': False}
GAMEB = {'names': ['B'], 'descriptions': ['B'],
         'game_types': ['song'], 'game_lengths': ['medium'], 'group_sizes': ['large'],
         'group_needs': [{'slug': 'groupid', 'score': 1}],
         'exhausting': False, 'touching': False, 'scalable': False, 'digital': False}
GAMEC = {'names': ['C'], 'descriptions': ['C'],
         'game_types': ['gtk'], 'game_lengths': ['long'], 'group_sizes': ['multiple'],
         'group_needs': [{'slug': 'groupid', 'score': 5}, {'slug': 'energy', 'score': 1}],
         'exhausting': False, 'touching': False, 'scalable': False, 'digital': False}


@pytest.fixture(scope='module', autouse=True)
def populate_with_abc(db):
    create_games([GAMEA, GAMEB, GAMEC])


def test_all_games_gt(db):
    query = {"game_type": "ice"}
    result = all_games(query)
    assert len(result) == 1
    assert result[0]['names'][0]['full'] == 'A'


def test_all_games_gl(db):
    query = {"game_length": "medium"}
    result = all_games(query)
    assert len(result) == 1
    assert result[0]['names'][0]['full'] == 'B'


def test_all_games_gs(db):
    query = {"group_size": "multiple"}
    result = all_games(query)
    assert len(result) == 1
    assert result[0]['names'][0]['full'] == 'C'


def test_all_games_gn():
    query = {"main": "groupid"}
    result = all_games(query)
    assert len(result) == 3
    assert result[0]['names'][0]['slug'] == 'c'
    assert result[1]['names'][0]['slug'] == 'a'
    assert result[2]['names'][0]['slug'] == 'b'

    query = {"main": "energy"}
    result = all_games(query)
    assert len(result) == 2
    assert result[0]['names'][0]['slug'] == 'a'
    assert result[1]['names'][0]['slug'] == 'c'

    query = {"main": "groupid", "limit": 2}
    result = all_games(query)
    assert len(result) == 2
    assert result[0]['names'][0]['slug'] == 'c'
    assert result[1]['names'][0]['slug'] == 'a'


def test_all_names_gt(db):
    query = {"game_type": "ice"}
    result = all_names(query)
    assert len(result) == 1
    assert result[0]['full'] == 'A'


def test_all_names_gl(db):
    query = {"game_length": "medium"}
    result = all_names(query)
    assert len(result) == 1
    assert result[0]['full'] == 'B'


def test_all_names_gs(db):
    query = {"group_size": "multiple"}
    result = all_names(query)
    assert len(result) == 1
    assert result[0]['full'] == 'C'


def test_all_names_gn():
    query = {"main": "groupid"}
    result = all_names(query)
    assert len(result) == 3
    assert result[0]['slug'] == 'c'
    assert result[1]['slug'] == 'a'
    assert result[2]['slug'] == 'b'

    query = {"main": "energy"}
    result = all_names(query)
    assert len(result) == 2
    assert result[0]['slug'] == 'a'
    assert result[1]['slug'] == 'c'

    query = {"main": "groupid", "limit": 2}
    result = all_names(query)
    assert len(result) == 2
    assert result[0]['slug'] == 'c'
    assert result[1]['slug'] == 'a'
