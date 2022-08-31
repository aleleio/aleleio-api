import os
from copy import deepcopy

MIN_GAME = {'names': ['Bananas'], 'descriptions': ['This stuff is bananas, BANANAS!'], 'game_types': ['ice', 'song'],
            'game_lengths': ['short'], 'group_sizes': ['event']}
MAX_GAME = {'names': ['Monkey Circus', 'Dog Show'], 'descriptions': ['This game has two descriptions.', 'Second one'],
            'game_types': ['ice', 'song'], 'game_lengths': ['short'], 'group_sizes': ['event'],
            'group_needs': [{'slug': 'why', 'score': 4}], 'materials': ['bananas', 'bones'],
            'prior_prep': 'Prepare the area by hiding both, bananas and bones.',
            'exhausting': True, 'touching': True, 'scalable': True, 'digital': True,
            'license': {'name': 'Unlicense', 'url': 'https://unlicense', 'owner': 'alele.io', 'owner_url': 'alele.io'},
            'references': [{'name': 'Wikipedia', 'url': 'https://wikipedia.org/monkey_circus'}]}


def test_get_games(client):
    response = client.get('/games')
    assert response.status_code == 200
    assert response.json == []


def test_create_games_with_complete_request(client):
    payload = [MIN_GAME]
    response = client.post('/games', json=payload)
    assert response.status_code == 201


def test_create_games_with_maximum_request(client):
    payload = [MAX_GAME]
    response = client.post('/games', json=payload)
    assert response.status_code == 201


def test_create_games_with_duplicate(client):
    payload = [MIN_GAME]
    response = client.post('/games', json=payload)
    assert response.status_code == 409
    assert response.json == {"errors": ["Cannot create Name: value 'bananas' for key slug already exists"]}


def test_create_games_empty_json(client):
    response = client.post('/games', json=[{}])
    assert response.status_code == 400
    assert 'is a required property' in response.text


def test_create_games_without_array(client):
    payload = MIN_GAME
    response = client.post('/games', json=payload)
    assert response.status_code == 400
    assert 'is not of type \'array\'' in response.text


def test_create_games_with_additional_properties(client):
    payload = deepcopy(MIN_GAME)
    payload['eek'] = 'A mouse!'
    response = client.post('/games', json=[payload])
    assert response.status_code == 400
    assert 'Additional properties are not allowed' in response.text


def test_get_single_game(client):
    response = client.get('/games/1')
    assert response.status_code == 200


def test_get_single_game_wrong_id(client):
    response = client.get('/games/99')
    assert response.status_code == 404


def test_update_game_name(client):
    payload = {"names": []}
    response = client.patch('/games/1', json=payload)
    assert response.status_code == 400
    assert '[] is too short - \'names\'' in response.text
    payload = {"names": ["kiwis"]}
    response = client.patch('/games/1', json=payload)
    assert response.status_code == 200
    assert response.json["names"][0]["slug"] == "kiwis"
    payload = {"names": ["bananas"]}
    response = client.patch('/games/1', json=payload)
    assert response.json["names"][0]["slug"] == "bananas"


def test_update_game_descriptions(client):
    payload = {"descriptions": []}
    response = client.patch('/games/2', json=payload)
    assert response.status_code == 400
    assert '[] is too short - \'descriptions\'' in response.text
    payload = {"descriptions": ["This game has two descriptions.", "Second one"]}
    response = client.patch('/games/2', json=payload)
    assert len(response.json["descriptions"]) == 2


def test_update_game_group_needs(client):
    payload = {"group_needs": []}
    response = client.patch('/games/2', json=payload)
    assert response.status_code == 200
    assert len(response.json["group_needs"]) == 0
    payload = {"group_needs": [{"slug": "groupid", "score": 4}, {"slug": "why", "score": 4}]}
    response = client.patch('/games/2', json=payload)
    assert len(response.json["group_needs"]) == 2
    assert {"slug": "groupid", "value": 4} in response.json["group_needs"]
    payload = {"group_needs": [{"slug": "why", "score": 4}]}
    response = client.patch('/games/2', json=payload)
    assert response.json["group_needs"][0]["slug"] == "why"


def test_update_game_with_minimal_license(client):
    payload = {"license": {"name": "MIT"}}
    response = client.patch('/games/2', json=payload)
    for item in (('name', 'MIT'), ('url', ''), ('owner', 'alele.io'), ('owner_url', 'https://alele.io')):
        assert item in response.json['license'].items()


def test_update_game_with_empty_game_types(client):
    """Games need at least one game_type
    """
    payload = {"game_types": []}
    response = client.patch('/games/1', json=payload)
    assert response.status_code == 400
    assert '[] is too short - \'game_types\'' in response.text


def test_update_game_with_wrong_id(client):
    payload = {}
    response = client.patch("/games/5", json=payload)
    assert response.status_code == 404
    assert response.json == {'detail': 'The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.', 'status': 404, 'title': 'Not Found', 'type': 'about:blank'}


def test_update_game_with_name_duplicate(client):
    payload = {'names':['Dog Show']}
    response = client.patch("/games/1", json=payload)
    assert response.status_code == 409
    assert response.json == {"errors": ["Cannot create Name: value 'dog-show' for key slug already exists"]}


def test_update_game_with_multiple_patches(client):
    payload = {}


def test_delete_single_game(client):
    response = client.get('/games')
    assert len(response.json) == 2
    response = client.delete('/games/1')
    assert response.status_code == 200
    response = client.get('/games')
    assert len(response.json) == 1
    response = client.delete('/games/2')
    assert response.status_code == 200
    response = client.get('/games')
    assert len(response.json) == 0
    client.post('/games', json=[MIN_GAME, MAX_GAME])


def test_delete_single_game_wrong_id(client):
    response = client.delete('/games/1')
    assert response.status_code == 404


