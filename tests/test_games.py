def test_create_game_view(client):
    response = client.get("/games")
    assert response.status_code == 200
    # assert response.json() == {}