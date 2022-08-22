import pytest
from pony.orm import db_session

from src.services.create import slugify, create_game_bools, create_game_relationships


def test_slugify_basic():
    assert slugify('Bananas') == 'bananas'
    assert slugify('We Got Bananas') == 'we-got-bananas'
    assert slugify('We-Got-Bananas') == 'we-got-bananas'
    assert slugify('Do we?_!)') == 'do-we'


def test_slugify_utf():
    assert slugify('ÄäÖöÜüß') == 'aaoouu'


@db_session
def test_create_game_bools(db):
    game = db.Game(license=db.License())
    request = {'exhausting': True, 'touching': False, 'scalable': True, 'digital': False}
    create_game_bools(game, request)
    assert game.exhausting is True
    assert game.touching is False
    assert game.scalable is True
    assert game.digital is False
    game.delete()


@db_session
def test_create_game_relationships(db):
    game = db.Game(license=db.License())
    request = {'game_types': ['ice', 'ener', 'trust', 'prob', 'name', 'brain', 'song'],
               'game_lengths': ['short', 'medium', 'long'],
               'group_sizes': ['small', 'large', 'multiple', 'event']}
    create_game_relationships(game, request)

