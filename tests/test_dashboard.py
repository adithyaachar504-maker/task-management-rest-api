"""Tests for dashboard analytics and smart task endpoints."""

from datetime import date, timedelta


def test_dashboard_stats(client):
    """Test GET /dashboard/stats calculates accurate statistics and completion rate."""
    client.post("/tasks", json={"title": "T1", "category": "Work", "priority": "high", "status": "completed"})
    client.post("/tasks", json={"title": "T2", "category": "Work", "priority": "medium", "status": "completed"})
    client.post("/tasks", json={"title": "T3", "category": "Study", "priority": "low", "status": "pending"})
    client.post("/tasks", json={"title": "T4", "category": "Personal", "priority": "medium", "status": "in_progress"})

    response = client.get("/dashboard/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["total_tasks"] == 4
    assert data["completed_tasks"] == 2
    assert data["pending_tasks"] == 1
    assert data["in_progress_tasks"] == 1
    assert data["completion_rate"] == 50.0


def test_dashboard_priority_summary(client):
    """Test GET /dashboard/priority-summary returns counts by priority."""
    client.post("/tasks", json={"title": "T1", "category": "Work", "priority": "low"})
    client.post("/tasks", json={"title": "T2", "category": "Work", "priority": "medium"})
    client.post("/tasks", json={"title": "T3", "category": "Work", "priority": "high"})
    client.post("/tasks", json={"title": "T4", "category": "Work", "priority": "high"})

    response = client.get("/dashboard/priority-summary")
    assert response.status_code == 200
    data = response.json()
    assert data["low"] == 1
    assert data["medium"] == 1
    assert data["high"] == 2


def test_dashboard_category_summary(client):
    """Test GET /dashboard/category-summary returns counts by category."""
    client.post("/tasks", json={"title": "T1", "category": "Work", "priority": "low"})
    client.post("/tasks", json={"title": "T2", "category": "Study", "priority": "low"})
    client.post("/tasks", json={"title": "T3", "category": "Personal", "priority": "low"})
    client.post("/tasks", json={"title": "T4", "category": "Project", "priority": "low"})

    response = client.get("/dashboard/category-summary")
    assert response.status_code == 200
    data = response.json()
    assert data["Work"] == 1
    assert data["Study"] == 1
    assert data["Personal"] == 1
    assert data["Project"] == 1


def test_overdue_tasks(client):
    """Test GET /tasks/overdue returns tasks whose due date has passed."""
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    tomorrow = (date.today() + timedelta(days=1)).isoformat()

    # Overdue task (pending)
    client.post("/tasks", json={"title": "Overdue Task", "category": "Work", "priority": "high", "due_date": yesterday})
    # Future task
    client.post("/tasks", json={"title": "Future Task", "category": "Work", "priority": "high", "due_date": tomorrow})
    # Completed task (due yesterday, but finished)
    client.post("/tasks", json={"title": "Done Task", "category": "Work", "priority": "high", "due_date": yesterday, "status": "completed"})

    response = client.get("/tasks/overdue")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Overdue Task"


def test_today_tasks(client):
    """Test GET /tasks/today returns tasks due today."""
    today = date.today().isoformat()
    tomorrow = (date.today() + timedelta(days=1)).isoformat()

    client.post("/tasks", json={"title": "Due Today Task", "category": "Study", "priority": "medium", "due_date": today})
    client.post("/tasks", json={"title": "Due Tomorrow Task", "category": "Study", "priority": "medium", "due_date": tomorrow})

    response = client.get("/tasks/today")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Due Today Task"
