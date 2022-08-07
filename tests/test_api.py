

def test_games(client):
    response = client.get('/games')
    assert response.status_code == 200
