from pathlib import Path

import pytest
from flask import g

from src.start import get_project_version


def test_about(client):
    response = client.get("/about")
    assert response.json == {"version": get_project_version(), "games": 0}


def test_import(client):
    print(f"{g.get('uid')=}")
    response = client.get("/import")
    assert response.status_code == 200
    # Todo: Test response
    # assert response.json == {}


def test_import_from_github(client, monkeypatch):
    def mock_is_latest_version():
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


@pytest.mark.no_mock_set_sha
@pytest.mark.no_mock_get_sha
def test_latest_sha(client, monkeypatch):
    from src.services import import_to_db, export_to_repo
    test_root = Path(__file__).parent.parent  # /tests
    monkeypatch.setattr(export_to_repo, "ROOT", test_root)

    def mock_is_latest_version():
        return True

    class MockRequests:
        @staticmethod
        def get(url, headers, allow_redirects):
            return MockRequests.Request()

        class Request:
            def json(self):
                return [{"sha": "1234567"}]

    monkeypatch.setattr(import_to_db, "is_latest_version", mock_is_latest_version)
    monkeypatch.setattr(export_to_repo, "requests", MockRequests)
    response = client.get("/import")
    assert response.json == {"result": 200}
    latest_sha_file = test_root.joinpath('.latest-sha')
    assert latest_sha_file.exists()
    latest_sha_file.unlink()

