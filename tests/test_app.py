
import pytest
from fastapi import status
from src.app import app, activities
from fastapi.testclient import TestClient

@pytest.fixture(autouse=True)
def reset_activities():
    # Arrange: Reset the in-memory activities before each test
    for activity in activities.values():
        activity["participants"] = activity["participants"][:2]  # Reset to initial state (first 2)

def test_get_activities():
    # Arrange: (nothing to set up)
    with TestClient(app) as client:
        # Act
        response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_for_activity():
    # Arrange
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    with TestClient(app) as client:
        # Act
        response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert email in activities[activity]["participants"]

def test_signup_duplicate():
    # Arrange
    email = activities["Chess Club"]["participants"][0]
    activity = "Chess Club"
    with TestClient(app) as client:
        # Act
        response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"

def test_unregister_participant():
    # Arrange
    email = activities["Chess Club"]["participants"][0]
    activity = "Chess Club"
    with TestClient(app) as client:
        # Act
        response = client.delete(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 200
    assert email not in activities[activity]["participants"]

def test_unregister_nonexistent_participant():
    # Arrange
    email = "notfound@mergington.edu"
    activity = "Chess Club"
    with TestClient(app) as client:
        # Act
        response = client.delete(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"
