import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert all('description' in v and 'participants' in v for v in data.values())

def test_signup_and_unregister():
    # Use a test email and activity
    test_email = "pytestuser@mergington.edu"
    activity_name = next(iter(client.get("/activities").json().keys()))

    # Sign up
    signup_resp = client.post(f"/activities/{activity_name}/signup?email={test_email}")
    assert signup_resp.status_code == 200
    assert "message" in signup_resp.json()

    # Check participant is added
    activities = client.get("/activities").json()
    assert test_email in activities[activity_name]["participants"]

    # Unregister
    unregister_resp = client.post(f"/activities/{activity_name}/unregister?email={test_email}")
    assert unregister_resp.status_code == 200
    assert "message" in unregister_resp.json()

    # Check participant is removed
    activities = client.get("/activities").json()
    assert test_email not in activities[activity_name]["participants"]

def test_signup_duplicate():
    test_email = "pytestdupe@mergington.edu"
    activity_name = next(iter(client.get("/activities").json().keys()))
    # Sign up once
    client.post(f"/activities/{activity_name}/signup?email={test_email}")
    # Sign up again (should fail or not duplicate)
    resp = client.post(f"/activities/{activity_name}/signup?email={test_email}")
    assert resp.status_code != 500  # Should not error
    # Clean up
    client.post(f"/activities/{activity_name}/unregister?email={test_email}")
