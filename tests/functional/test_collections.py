def test_get_collections(client):
    # ToDo: NotImplemented
    response = client.get('collections')
    assert response.status_code == 200


def test_create_collections(client):
    # ToDo: NotImplemented
    payload = []
    response = client.post('collections', json=payload)
    assert response.status_code == 204
