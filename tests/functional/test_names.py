def test_get_names(client):
    response = client.get('/names')
    assert response.status_code == 200


