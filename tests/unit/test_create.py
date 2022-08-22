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
    gt1 = db.GameType.get(slug='brain')
    gl1 = db.GameLength.get(slug='long')
    gs1 = db.GroupSize.get(slug='small')
    assert gt1 in game.game_types.select()[:]
    assert gl1 in game.game_lengths.select()[:]
    assert gs1 in game.group_sizes.select()[:]


@db_session
def test_create_game_relationships_with_group_needs(db):
    game = db.Game(license=db.License())
    request = {"game_types": ["trust"],
               "game_lengths": ["long"],
               "group_sizes": ["small"],
               "group_needs": [{"slug": "first", "score": 5}, {"slug": "honesty", "score": 0}]}
    create_game_relationships(game, request)
    gn1 = db.GroupNeed.get(slug="honesty")
    gns1 = db.GroupNeedScore.get(lambda gns: gns.game is game and gns.group_need is gn1)
    assert gns1.value == 0
    assert len(game.group_need_scores.select()) == 2