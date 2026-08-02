from urllib.parse import quote

from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_get_activities_returns_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    activities = response.json()
    assert "Chess Club" in activities
    assert "participants" in activities["Chess Club"]


def test_signup_and_unregister_participant():
    activity_name = "Chess Club"
    test_email = "test.user@example.com"

    signup_response = client.post(
        f"/activities/{quote(activity_name)}/signup",
        params={"email": test_email},
    )
    assert signup_response.status_code == 200
    assert test_email in signup_response.json()["message"]

    activities_response = client.get("/activities")
    assert activities_response.status_code == 200
    assert test_email in activities_response.json()[activity_name]["participants"]

    delete_response = client.delete(
        f"/activities/{quote(activity_name)}/signup",
        params={"email": test_email},
    )
    assert delete_response.status_code == 200
    assert test_email in delete_response.json()["message"]

    final_response = client.get("/activities")
    assert final_response.status_code == 200
    assert test_email not in final_response.json()[activity_name]["participants"]


def test_signup_duplicate_returns_error():
    activity_name = "Programming Class"
    existing_email = "emma@mergington.edu"

    duplicate_response = client.post(
        f"/activities/{quote(activity_name)}/signup",
        params={"email": existing_email},
    )
    assert duplicate_response.status_code == 400
    assert "already signed up" in duplicate_response.json()["detail"].lower()
