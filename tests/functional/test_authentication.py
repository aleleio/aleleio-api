def test_regular_route(client):
    response = client.get("/games")
    assert response.status_code == 200


def test_missing_headers(no_auth_client):
    response = no_auth_client.get("/games")
    assert response.status_code == 401