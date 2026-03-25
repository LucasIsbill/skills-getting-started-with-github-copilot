"""
Tests for the GET /activities endpoint
"""

import pytest


def test_get_activities_returns_all_activities(client):
    """Test that GET /activities returns all activities with correct structure"""
    response = client.get("/activities")
    
    assert response.status_code == 200
    activities = response.json()
    
    # Should have 9 activities
    assert len(activities) == 9
    
    # Check that expected activities are present
    expected_activities = [
        "Chess Club", "Programming Class", "Gym Class", "Basketball Team",
        "Tennis Club", "Art Studio", "Drama Club", "Debate Team", "Science Club"
    ]
    for activity in expected_activities:
        assert activity in activities


def test_activity_has_required_fields(client):
    """Test that each activity has the required fields"""
    response = client.get("/activities")
    activities = response.json()
    
    required_fields = ["description", "schedule", "max_participants", "participants"]
    
    for activity_name, activity_data in activities.items():
        for field in required_fields:
            assert field in activity_data, f"Activity '{activity_name}' missing field '{field}'"


def test_activity_participants_is_list(client):
    """Test that participants field is always a list"""
    response = client.get("/activities")
    activities = response.json()
    
    for activity_name, activity_data in activities.items():
        assert isinstance(activity_data["participants"], list), \
            f"Participants for '{activity_name}' is not a list"


def test_activity_max_participants_is_integer(client):
    """Test that max_participants is an integer"""
    response = client.get("/activities")
    activities = response.json()
    
    for activity_name, activity_data in activities.items():
        assert isinstance(activity_data["max_participants"], int), \
            f"max_participants for '{activity_name}' is not an integer"
