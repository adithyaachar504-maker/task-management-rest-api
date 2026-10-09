"""Tests for deleting tasks DELETE /tasks/{id}."""


def test_delete_task_success(client):
    """Test deleting an existing task returns 204 status code."""
    created = client.post(
        "/tasks", json={"title": "Task to Delete", "category": "Project", "priority": "low"}
    ).json()

    task_id = created["id"]
    delete_response = client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == 204

    # Verify task is deleted
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404


def test_delete_non_existing_task(client):
    """Test deleting a non-existing task returns 404."""
    response = client.delete("/tasks/9999")
    assert response.status_code == 404
    data = response.json()
    assert data["error"] == "Task not found"
