"""Tests for retrieving tasks endpoints GET /tasks and GET /tasks/{task_id}."""


def test_get_tasks_empty(client):
    """Test retrieving tasks when database is empty."""
    response = client.get("/tasks")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert data["page"] == 1
    assert data["limit"] == 10
    assert data["tasks"] == []


def test_get_tasks_list(client):
    """Test retrieving all created tasks."""
    client.post("/tasks", json={"title": "Task 1", "category": "Work", "priority": "low"})
    client.post("/tasks", json={"title": "Task 2", "category": "Study", "priority": "medium"})

    response = client.get("/tasks")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert len(data["tasks"]) == 2


def test_get_task_by_id_success(client):
    """Test getting a task by its valid ID."""
    created = client.post(
        "/tasks", json={"title": "Specific Task", "category": "Personal", "priority": "high"}
    ).json()

    task_id = created["id"]
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Specific Task"


def test_get_non_existing_task(client):
    """Test getting a non-existing task returns 404."""
    response = client.get("/tasks/9999")
    assert response.status_code == 404
    data = response.json()
    assert "error" in data
    assert data["status_code"] == 404
    assert data["error"] == "Task not found"
