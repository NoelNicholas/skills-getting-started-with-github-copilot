from fastapi.testclient import TestClient
from src import app as app_module
import copy

client = TestClient(app_module.app)
# Snapshot initial activities to restore between tests
_initial_activities = copy.deepcopy(app_module.activities)

import pytest

@pytest.fixture(autouse=True)
def reset_activities():
    # Restore a fresh copy before each test
    app_module.activities = copy.deepcopy(_initial_activities)
    yield


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # Check a known activity exists
    assert "Chess Club" in data


def test_signup_and_duplicate():
    email = "tester@mergington.edu"
    from fastapi.testclient import TestClient
    from src import app as app_module
    import copy

    client = TestClient(app_module.app)
    # Snapshot initial activities to restore between tests
    _initial_activities = copy.deepcopy(app_module.activities)

    import pytest

    @pytest.fixture(autouse=True)
    def reset_activities():
        # Restore a fresh copy before each test
        app_module.activities = copy.deepcopy(_initial_activities)
        yield


    def test_get_activities():
        resp = client.get("/activities")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, dict)
        # Check a known activity exists
        assert "Chess Club" in data


    def test_signup_and_duplicate():
        email = "tester@mergington.edu"
        activity = "Chess Club"

        # Sign up should succeed
        resp = client.post(f"/activities/{activity}/signup?email={email}")
        assert resp.status_code == 200
        assert "Signed up" in resp.json().get("message", "")

        # Participant should be present in activities
        data = client.get("/activities").json()
        assert email in data[activity]["participants"]

        # Duplicate signup should fail with 400
        resp2 = client.post(f"/activities/{activity}/signup?email={email}")
        assert resp2.status_code == 400
        assert "already signed up" in resp2.json().get("detail", "").lower()


    def test_remove_participant():
        # Use an existing participant from initial data
        activity = "Chess Club"
        existing = _initial_activities[activity]["participants"][0]

        # Remove existing participant
        resp = client.delete(f"/activities/{activity}/participants?email={existing}")
        assert resp.status_code == 200
        assert "Removed" in resp.json().get("message", "")

        # Verify participant removed
        data = client.get("/activities").json()
        assert existing not in data[activity]["participants"]

        # Removing again should return 404
        resp2 = client.delete(f"/activities/{activity}/participants?email={existing}")
        assert resp2.status_code == 404