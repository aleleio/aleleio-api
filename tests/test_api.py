import os
from copy import deepcopy

GAME1 = {'names': ['Bananas'], 'descriptions': ['This stuff is bananas, BANANAS!'], 'game_types': ['ice', 'song'],
               'game_lengths': ['short'], 'group_sizes': ['event']}


def test_get_games(client):
    response = client.get('/games')
    # print(response.text)
    assert response.status_code == 200


def test_create_games_empty_json(client):
    response = client.post('/games', json=[{}])
    assert response.status_code == 400
    assert 'is a required property' in response.text


def test_create_games_without_array(client):
    payload = GAME1
    response = client.post('/games', json=payload)
    assert response.status_code == 400
    assert 'is not of type \'array\'' in response.text


def test_create_games_with_additional_properties(client):
    payload = deepcopy(GAME1)
    payload['eek'] = 'A mouse!'
    response = client.post('/games', json=[payload])
    assert response.status_code == 400
    assert 'Additional properties are not allowed' in response.text


def test_create_games_with_complete_request(client):
    payload = [GAME1]
    response = client.post('/games', json=payload)
    assert response.status_code == 201
