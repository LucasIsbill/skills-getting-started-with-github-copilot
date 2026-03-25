"""
Tests for the POST /activities/{activity_name}/signup endpoint
"""

import pytest


def test_signup_success(client):
    """Test successful signup to an activity"""
    response = client.post(
        "/activities/Chess%20Club/signup?email=newstudent@mergington.edu"
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "newstudent@mergington.edu" in data["message"]
    assert "Chess Club" in data["message"]


def test_signup_adds_participant(client):
    """Test that signup actually adds the participant to the activity"""
    email = "testuser@mergington.edu"
    
    # Sign up
    response = client.post(
        "/activities/Programming%20Class/signup",
        params={"email": email}
    )
    assert response.status_code == 200
    
    # Verify participant was added
    activities = client.get("/activities").json()
    assert email in activities["Programming Class"]["participants"]


def test_signup_duplicate_email_returns_400(client):
    """Test that signing up the same email twice returns a 400 error"""
    email = "michael@mergington.edu"  # Already signed up for Chess Club
    
    response = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": email}
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"].lower()


def test_signup_nonexistent_activity_returns_404(client):
    """Test that signing up for a non-existent activity returns a 404 error"""
    response = client.post(
        "/activities/NonExistent%20Activity/signup",
        params={"email": "student@mergington.edu"}
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_signup_multiple_different_students(client):
    """Test that multiple different students can sign up for the same activity"""
    activity = "Art%20Studio"
    emails = ["student1@mergington.edu", "student2@mergington.edu"]
    
    for email in emails:
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        assert response.status_code == 200
    
    # Verify both were added
    activities = client.get("/activities").json()
    for email in emails:
        assert email in activities["Art Studio"]["participants"]


def test_signup_with_special_characters_in_email(client):
    """Test signup with an email containing special characters"""
    email = "student+test@mergington.edu"
    
    response = client.post(
        "/activities/Debate%20Team/signup",
        params={"email": email}
    )
    
    assert response.status_code == 200
    
    # Verify participant was added
    activities = client.get("/activities").json()
    assert email in activities["Debate Team"]["participants"]
