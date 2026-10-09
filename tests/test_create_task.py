"""Tests for task creation endpoint POST /tasks."""


def test_create_task_success(client):
    """Test creating a task with valid minimal required fields."""
    payload = {
        "title": "Learn FastAPI",
        "category": "Study",
        "priority": "high",
    }
    response = client.post("/tasks", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["title"] == "Learn FastAPI"
    assert data["category"] == "Study"
    assert data["priority"] == "high"
    assert data["status"] == "pending"
    assert "created_at" in data
    assert "updated_at" in data


def test_create_task_all_fields(client):
    """Test creating a task with all fields explicitly defined."""
    payload = {
        "title": "Complete Internship Project",
        "description": "Build FastAPI REST API and test suite",
        "category": "Project",
        "priority": "high",
        "status": "in_progress",
        "due_date": "2026-10-15",
    }
    response = client.post("/tasks", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Complete Internship Project"
    assert data["description"] == "Build FastAPI REST API and test suite"
    assert data["category"] == "Project"
    assert data["priority"] == "high"
    assert data["status"] == "in_progress"
    assert data["due_date"] == "2026-10-15"
