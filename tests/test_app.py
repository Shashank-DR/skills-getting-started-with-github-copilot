import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_read_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    activities = response.json()
    assert "Chess Club" in activities
    assert "Programming Class" in activities
    assert isinstance(activities["Chess Club"]["participants"], list)

def test_signup_for_activity():
    # Test successful signup
    response = client.post("/activities/Chess Club/signup?email=test@mergington.edu")
    assert response.status_code == 200
    assert "Signed up test@mergington.edu for Chess Club" in response.json()["message"]
    
    # Test duplicate signup
    response = client.post("/activities/Chess Club/signup?email=test@mergington.edu")
    assert response.status_code == 400
    assert "Student already signed up for this activity" in response.json()["detail"]
    
    # Test signup for non-existent activity
    response = client.post("/activities/NonexistentClub/signup?email=test@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]

def test_unregister_from_activity():
    # First sign up a test user
    email = "unregister_test@mergington.edu"
    client.post(f"/activities/Chess Club/signup?email={email}")
    
    # Test successful unregistration
    response = client.post(f"/activities/Chess Club/unregister?email={email}")
    assert response.status_code == 200
    assert f"Successfully unregistered from Chess Club" in response.json()["message"]
    
    # Test unregister when not registered
    response = client.post(f"/activities/Chess Club/unregister?email={email}")
    assert response.status_code == 400
    assert "Student is not registered for this activity" in response.json()["detail"]
    
    # Test unregister from non-existent activity
    response = client.post(f"/activities/NonexistentClub/unregister?email={email}")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]