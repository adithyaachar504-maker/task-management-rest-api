"""Tests for search, filtering, and pagination on GET /tasks."""


def setup_sample_tasks(client):
    """Helper fixture setup for populating tasks."""
    tasks = [
        {"title": "Python Basics", "description": "Study variables and loops", "category": "Study", "priority": "high", "status": "pending"},
        {"title": "FastAPI Project", "description": "Build python REST backend", "category": "Project", "priority": "high", "status": "in_progress"},
        {"title": "Buy Groceries", "description": "Milk, eggs, bread", "category": "Personal", "priority": "low", "status": "pending"},
        {"title": "Work Meeting", "description": "Sprint planning session", "category": "Work", "priority": "medium", "status": "completed"},
    ]
    for t in tasks:
        client.post("/tasks", json=t)


def test_filter_by_status(client):
    """Test filtering tasks by status=pending."""
    setup_sample_tasks(client)
    response = client.get("/tasks?status=pending")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    for task in data["tasks"]:
        assert task["status"] == "pending"


def test_filter_by_priority(client):
    """Test filtering tasks by priority=high."""
    setup_sample_tasks(client)
    response = client.get("/tasks?priority=high")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    for task in data["tasks"]:
        assert task["priority"] == "high"


def test_filter_by_category(client):
    """Test filtering tasks by category=Study."""
    setup_sample_tasks(client)
    response = client.get("/tasks?category=Study")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["tasks"][0]["category"] == "Study"


def test_search_tasks(client):
    """Test searching tasks with keyword search=python."""
    setup_sample_tasks(client)
    response = client.get("/tasks?search=python")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    for task in data["tasks"]:
        assert "python" in task["title"].lower() or "python" in task["description"].lower()


def test_multiple_filters(client):
    """Test combining status and priority filters."""
    setup_sample_tasks(client)
    response = client.get("/tasks?status=pending&priority=high")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["tasks"][0]["title"] == "Python Basics"


def test_pagination(client):
    """Test task pagination parameters page and limit."""
    setup_sample_tasks(client)
    response = client.get("/tasks?page=1&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 4
    assert data["page"] == 1
    assert data["limit"] == 2
    assert data["total_pages"] == 2
    assert len(data["tasks"]) == 2

    # Page 2
    response_page2 = client.get("/tasks?page=2&limit=2")
    assert response_page2.status_code == 200
    data_page2 = response_page2.json()
    assert len(data_page2["tasks"]) == 2
