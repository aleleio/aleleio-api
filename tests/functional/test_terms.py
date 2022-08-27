def test_get_references(client):
    response = client.get('/references')
    assert response.status_code == 200


def test_create_references(client):
    payload = [{"name": "Alelchen", "url": "https://alele.io", "refers-to": "alele"}]
    response = client.post('/references', json=payload)
    assert response.status_code == 200


def test_get_collections(client):
    # ToDo: NotImplemented
    response = client.get('collections')
    assert response.status_code == 204


def test_create_collections(client):
    # ToDo: NotImplemented
    payload = []
    response = client.post('collections', json=payload)
    assert response.status_code == 204
