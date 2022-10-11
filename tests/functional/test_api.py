from datetime import datetime
from pathlib import Path

import pytest


def test_about(client):
    response = client.get("/about")
    assert response.status_code == 200
    # assert response.json == {"version": get_project_version(), "games": 0}


def test_import(client):
    response = client.get("/import")
    assert response.status_code == 200
    assert ("errors", []) in response.json["games"].items()
    assert ("len", 5) in response.json["games"].items()
    assert ("errors", []) in response.json["refs"].items()
    assert ("len", 2) in response.json["refs"].items()


def test_is_not_latest_version(client, monkeypatch):
    def mock_is_latest_version(sha):
        return False
    class MockRequests:
        @staticmethod
        def get(url, headers, allow_redirects):
            return MockRequests.Request()
        class Request:
            def __init__(self):
                self.status_code = 200
                self.headers = {"content-disposition": "zipfile 012346789aleleio-teambuilding-games-12345671234"}
                self.content = b"some content"
    class MockZipFile:
        def __init__(self, path, mode):
            pass
        def __enter__(self):
            return self
        def __exit__(self, one, two, three):
            pass
        def extractall(self, path):
            pass
    from src.services import import_to_db
    monkeypatch.setattr(import_to_db, "is_latest_version", mock_is_latest_version)
    monkeypatch.setattr(import_to_db, "requests", MockRequests)
    monkeypatch.setattr(import_to_db, "ZipFile", MockZipFile)
    response = client.get("/import")
    assert response.status_code == 200
    assert ("errors", []) in response.json["games"].items()
    assert ("len", 5) in response.json["games"].items()
    assert ("created", []) in response.json["refs"].items()
    assert ("len", 0) in response.json["refs"].items()


@pytest.mark.no_mock_set_sha
@pytest.mark.no_mock_get_sha
def test_is_latest_version(client, monkeypatch):
    def mock_is_latest_version(sha):
        return True

    class MockRequests:
        @staticmethod
        def get(url, headers, allow_redirects):
            return MockRequests.Request()

        class Request:
            def json(self):
                return [{"sha": "1234567"}]

    from src.services import connect_github
    monkeypatch.setattr(connect_github, "is_latest_version", mock_is_latest_version)
    monkeypatch.setattr(connect_github, "requests", MockRequests)
    response = client.get("/import")
    assert response.status_code == 200
    print()
    # test_root = Path(__file__).parent.parent  # /tests
    # latest_sha_file = test_root.joinpath('.latest-sha')
    # assert latest_sha_file.exists()
    # latest_sha_file.unlink()


@pytest.mark.parametrize("name", [("api", "aleleio-api"), ("web", "aleleio-web"), ("teambuilding-games", "teambuilding-games")])
def test_github_action_request_import(client, name):
    client.post("/import", json={"name": name[1]})
    r = client.get("/about")
    assert r.json[name[0]]["last_commit"] == datetime.strftime(datetime(1987, 1, 25, 2, 33, 44), "%Y-%m-%dT%H:%M:%SZ")