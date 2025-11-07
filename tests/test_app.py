from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    # Basic sanity checks
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_remove_participant():
    activity = "Chess Club"
    email = "testuser@example.com"

    # Ensure email not already present
    resp = client.get("/activities")
    assert resp.status_code == 200
    activities = resp.json()
    assert email not in activities[activity]["participants"]

    # Sign up
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    assert "Signed up" in resp.json().get("message", "")

    # Verify participant present
    resp = client.get("/activities")
    activities = resp.json()
    assert email in activities[activity]["participants"]

    # Remove participant
    resp = client.delete(f"/activities/{activity}/participants/{email}")
    assert resp.status_code == 200
    assert "Removed" in resp.json().get("message", "")

    # Verify removed
    resp = client.get("/activities")
    activities = resp.json()
    assert email not in activities[activity]["participants"]


def test_signup_already_signed():
    activity = "Chess Club"
    existing_email = "michael@mergington.edu"

    resp = client.post(f"/activities/{activity}/signup?email={existing_email}")
    # The API returns 400 if already signed up
    assert resp.status_code == 400


def test_activity_not_found():
    resp = client.post("/activities/NoSuchActivity/signup?email=me@example.com")
    assert resp.status_code == 404
