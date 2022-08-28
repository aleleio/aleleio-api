import pytest

from src.services.create import create_games

MIN_GAME = {'names': ['Bananas'], 'descriptions': ['This stuff is bananas, BANANAS!'], 'game_types': ['ice', 'song'],
            'game_lengths': ['short'], 'group_sizes': ['event'],
            'exhausting': False, 'touching': False, 'scalable': False, 'digital': False}
REF_A = {"full": "Bananas Video", "url": "youtube.com/v=12345", "refers_to": "bananas"}


@pytest.fixture(autouse=True)
def populate_with_abc(db):
    create_games([MIN_GAME])


def test_create_references(client):
    response = client.post('references', json=[REF_A])
    assert response.status_code == 201
    assert response.json == [{"full": "Bananas Video",
                              "game": 1,
                              "id": 1,
                              "slug": "bananas-ref-0",
                              "url": "youtube.com/v=12345"}]


def test_create_references_with_duplicate(client):
    response = client.post('references', json=[REF_A])
    assert response.status_code == 409
    assert response.json == {'errors': ["Cannot create Reference: value 'youtube.com/v=12345' for key url already exists"]}


def test_get_references(client):
    response = client.get('/references')
    assert response.status_code == 200
    assert response.json == [{"full": "Bananas Video",
                              "game": 1,
                              "id": 1,
                              "slug": "bananas-ref-0",
                              "url": "youtube.com/v=12345"}]


def test_create_references_wrong_game(client):
    payload = [{"full": "A weird page", "url": "https://weird.url", "refers_to": "this-game-does-not-exist"}]
    response = client.post('/references', json=payload)
    assert response.status_code == 404
    assert "No game with slug None to refer to." in response.json['detail']
