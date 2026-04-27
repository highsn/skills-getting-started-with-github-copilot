from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_root_redirect():
    """Test root endpoint serves the index page."""
    # Arrange - no setup needed

    # Act
    response = client.get("/")

    # Assert
    assert response.status_code == 200
    assert "Mergington High School" in response.text


def test_get_activities():
    """Test retrieving all activities."""
    # Arrange - no setup needed

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "description" in data["Chess Club"]
    assert "participants" in data["Chess Club"]
    assert len(data["Chess Club"]["participants"]) == 2  # Initial count


def test_signup_success():
    """Test successful signup for an activity."""
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Signed up" in data["message"]
    assert email in data["message"]

    # Verify participant was added
    get_response = client.get("/activities")
    activities_data = get_response.json()
    assert email in activities_data[activity]["participants"]


def test_signup_duplicate():
    """Test signup fails for already enrolled student."""
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"  # Already enrolled

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"]


def test_signup_full_activity():
    """Test signup fails when activity is at max capacity."""
    # Arrange - Fill Chess Club (max 12, starts with 2)
    activity = "Chess Club"
    for i in range(10):  # Add 10 more to reach 12
        client.post(f"/activities/{activity}/signup?email=filler{i}@mergington.edu")

    email = "overflow@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "full" in data["detail"]


def test_signup_invalid_activity():
    """Test signup fails for nonexistent activity."""
    # Arrange
    activity = "Nonexistent Activity"
    email = "test@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"]


def test_unregister_success():
    """Test successful unregistration from an activity."""
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"  # Already enrolled

    # Act
    response = client.delete(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Unregistered" in data["message"]
    assert email in data["message"]

    # Verify participant was removed
    get_response = client.get("/activities")
    activities_data = get_response.json()
    assert email not in activities_data[activity]["participants"]


def test_unregister_not_enrolled():
    """Test unregister fails for student not enrolled."""
    # Arrange
    activity = "Chess Club"
    email = "notenrolled@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "not signed up" in data["detail"]


def test_unregister_invalid_activity():
    """Test unregister fails for nonexistent activity."""
    # Arrange
    activity = "Nonexistent Activity"
    email = "test@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"]