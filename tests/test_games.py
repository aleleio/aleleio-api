

def test_all_games_view_no_content(client):
    response = client.get("/games")
    assert response.status_code == 200
    assert response.json() == []


def test_single_game_view_no_content(client):
    response = client.get("/game/1")
    assert response.status_code == 404
