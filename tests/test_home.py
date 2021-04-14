from fastapi.testclient import TestClient

from src.main import api as app, configure


class Test:
    client = TestClient(app)
    configure()

    def test_index(self):
        response = self.client.get("/")
        assert response.status_code == 200
