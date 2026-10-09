"""Tests for Pydantic schema validation and error responses."""


def test_missing_title(client):
    """Test validation fails when title field is missing."""
    payload = {
        "category": "Work",
        "priority": "low",
    }
    response = client.post("/tasks", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert data["status_code"] == 422
    assert "error" in data


def test_empty_title(client):
    """Test validation fails when title is empty or whitespace only."""
    payload = {
        "title": "   ",
        "category": "Work",
        "priority": "low",
    }
    response = client.post("/tasks", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert data["status_code"] == 422


def test_invalid_priority(client):
    """Test validation fails when priority is not low, medium, or high."""
    payload = {
        "title": "Valid Title",
        "category": "Work",
        "priority": "critical",
    }
    response = client.post("/tasks", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert data["status_code"] == 422


def test_invalid_status(client):
    """Test validation fails when status is not pending, in_progress, or completed."""
    payload = {
        "title": "Valid Title",
        "category": "Work",
        "priority": "medium",
        "status": "archived",
    }
    response = client.post("/tasks", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert data["status_code"] == 422


def test_invalid_category(client):
    """Test validation fails when category is not Work, Study, Personal, or Project."""
    payload = {
        "title": "Valid Title",
        "category": "Entertainment",
        "priority": "medium",
    }
    response = client.post("/tasks", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert data["status_code"] == 422


def test_invalid_due_date_format(client):
    """Test validation fails when due_date is invalid date string."""
    payload = {
        "title": "Valid Title",
        "category": "Work",
        "priority": "medium",
        "due_date": "not-a-date",
    }
    response = client.post("/tasks", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert data["status_code"] == 422
