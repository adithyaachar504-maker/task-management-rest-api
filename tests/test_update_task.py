"""Tests for updating tasks PUT /tasks/{id} and PATCH /tasks/{id}/complete."""


def test_update_task_success(client):
    """Test updating task details using PUT endpoint."""
    created = client.post(
        "/tasks", json={"title": "Old Title", "category": "Work", "priority": "low"}
    ).json()

    task_id = created["id"]
    update_payload = {
        "title": "New Title",
        "priority": "high",
        "status": "in_progress",
    }
    response = client.put(f"/tasks/{task_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Title"
    assert data["priority"] == "high"
    assert data["status"] == "in_progress"
    assert data["category"] == "Work"  # preserved


def test_update_non_existing_task(client):
    """Test updating a non-existing task returns 404."""
    response = client.put("/tasks/9999", json={"title": "Test"})
    assert response.status_code == 404
    data = response.json()
    assert data["error"] == "Task not found"


def test_complete_task_success(client):
    """Test marking a task completed using PATCH /tasks/{id}/complete."""
    created = client.post(
        "/tasks", json={"title": "Task to Complete", "category": "Personal", "priority": "medium"}
    ).json()

    task_id = created["id"]
    response = client.patch(f"/tasks/{task_id}/complete")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "completed"


def test_complete_non_existing_task(client):
    """Test completing a non-existing task returns 404."""
    response = client.patch("/tasks/9999/complete")
    assert response.status_code == 404
    data = response.json()
    assert data["error"] == "Task not found"
