# SmartTask – Task Management & Productivity API

![Tests](https://github.com/USERNAME/REPOSITORY/actions/workflows/tests.yml/badge.svg)
![Python Version](https://img.shields.io/badge/Python-3.11%2B-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## Overview

**SmartTask** is a production-grade, feature-rich REST API built using **Python FastAPI**, **SQLAlchemy ORM**, **SQLite**, and **Pydantic**. Designed for real-world backend task management and team productivity tracking, SmartTask provides full task CRUD capabilities, keyword searching, status/priority/category filtering, page-based pagination, smart task detection (overdue & today's tasks), and real-time dashboard analytics.

This project was built to demonstrate backend software engineering practices suitable for a **BCA student's internship portfolio and GitHub showcase**.

Key competencies demonstrated in this codebase:
- **REST API Architecture & Design**
- **Modern Python Backend Development** (FastAPI, Python 3.11+)
- **ORM & Relational Database Integration** (SQLAlchemy 2.0, SQLite)
- **Data Schema Validation & Serialization** (Pydantic v2)
- **Automated Testing Suite** (Pytest, HTTPX, isolated in-memory DB)
- **Continuous Integration (CI/CD)** (GitHub Actions pipeline)
- **Interactive OpenAPI / Swagger Documentation**

---

## Features

- 📝 **Full Task CRUD**: Create, read, update, complete, and delete tasks.
- 🎯 **Domain Enums & Rules**: Strict validation on task priority (`low`, `medium`, `high`), status (`pending`, `in_progress`, `completed`), and category (`Work`, `Study`, `Personal`, `Project`).
- 🔍 **Search & Multi-Filtering**: Search by keyword in title/description and combine multiple filters simultaneously.
- 📄 **Pagination Envelope**: Structured response containing total items, total pages, current page, and page limit.
- ⚡ **Smart Endpoints**: Instantly retrieve overdue tasks or tasks scheduled for today.
- 📊 **Productivity Dashboard**: Aggregate statistics on total tasks, completion rates, priority distribution, and category summaries.
- 🛡️ **Consistent Error Format**: Standardized error payloads (`{"error": "...", "status_code": ...}`) across HTTP and validation exceptions.
- 🧪 **Comprehensive Automated Testing**: 100% test coverage across 26 test cases with isolated in-memory test database.
- 🚀 **GitHub Actions Pipeline**: Continuous integration workflow running unit tests on every push and pull request.

---

## Tech Stack

- **Language**: Python 3.11+
- **Framework**: FastAPI
- **Data Validation**: Pydantic v2
- **ORM**: SQLAlchemy 2.0
- **Database**: SQLite
- **Web Server**: Uvicorn
- **Testing**: Pytest & HTTPX / TestClient
- **CI/CD**: GitHub Actions
- **API Documentation**: OpenAPI, Swagger UI, ReDoc

---

## Architecture & Project Structure

```
smarttask-api/
│
├── app/
│   ├── __init__.py          # Package initialization
│   ├── main.py              # FastAPI app instance, exception handlers & health route
│   ├── database.py          # SQLAlchemy engine & session maker
│   ├── models.py            # Task database model definition
│   ├── schemas.py           # Pydantic schemas and Enums
│   ├── crud.py              # Database query logic & CRUD helpers
│   └── routers/
│       ├── __init__.py      # Routers package initialization
│       ├── tasks.py         # Task CRUD & smart endpoints router
│       └── dashboard.py     # Analytics & statistics router
│
├── tests/
│   ├── __init__.py          # Test package initialization
│   ├── conftest.py          # Pytest fixtures & isolated in-memory test DB
│   ├── test_root.py         # Health check tests
│   ├── test_create_task.py  # Task creation tests
│   ├── test_get_tasks.py    # Read task list and single task tests
│   ├── test_update_task.py  # Update & complete task tests
│   ├── test_delete_task.py  # Delete task tests
│   ├── test_filters.py      # Search, filter, and pagination tests
│   ├── test_dashboard.py    # Analytics & overdue/today tests
│   └── test_validation.py   # Schema validation rule tests
│
├── .github/
│   └── workflows/
│       └── tests.yml        # GitHub Actions CI workflow
│
├── requirements.txt         # Project dependencies
├── pytest.ini               # Pytest test runner configuration
├── .gitignore               # Git ignored files
└── README.md                # Project documentation
```

---

## API Endpoints

| Method | Endpoint | Tag | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/health` | Health | Service health check |
| `POST` | `/tasks` | Tasks | Create a new task |
| `GET` | `/tasks` | Tasks | List tasks (supports `status`, `priority`, `category`, `search`, `page`, `limit`) |
| `GET` | `/tasks/overdue` | Tasks | List overdue uncompleted tasks |
| `GET` | `/tasks/today` | Tasks | List tasks due today |
| `GET` | `/tasks/{task_id}` | Tasks | Retrieve single task by ID |
| `PUT` | `/tasks/{task_id}` | Tasks | Update an existing task |
| `PATCH` | `/tasks/{task_id}/complete` | Tasks | Mark task as completed |
| `DELETE` | `/tasks/{task_id}` | Tasks | Delete a task (HTTP 204) |
| `GET` | `/dashboard/stats` | Dashboard | Overall task counts & completion rate % |
| `GET` | `/dashboard/priority-summary` | Dashboard | Breakdown of tasks by priority level |
| `GET` | `/dashboard/category-summary` | Dashboard | Breakdown of tasks by category |

---

## Request & Response Examples

### 1. Create a Task
**Request**: `POST /tasks`
```json
{
  "title": "Build FastAPI REST API",
  "description": "Develop backend with SQLite and Pydantic validation",
  "category": "Project",
  "priority": "high",
  "status": "in_progress",
  "due_date": "2026-10-01"
}
```

**Response** (`HTTP 201 Created`):
```json
{
  "title": "Build FastAPI REST API",
  "description": "Develop backend with SQLite and Pydantic validation",
  "category": "Project",
  "priority": "high",
  "status": "in_progress",
  "due_date": "2026-10-01",
  "id": 1,
  "created_at": "2026-09-28T21:45:00.000000",
  "updated_at": "2026-09-28T21:45:00.000000"
}
```

### 2. Paginated & Filtered Tasks List
**Request**: `GET /tasks?status=pending&priority=high&page=1&limit=10`

**Response** (`HTTP 200 OK`):
```json
{
  "total": 1,
  "page": 1,
  "limit": 10,
  "total_pages": 1,
  "tasks": [
    {
      "id": 2,
      "title": "Study Python Algorithms",
      "description": "Practice recursion and sorting algorithms",
      "category": "Study",
      "priority": "high",
      "status": "pending",
      "due_date": "2026-09-30",
      "created_at": "2026-09-28T21:46:00.000000",
      "updated_at": "2026-09-28T21:46:00.000000"
    }
  ]
}
```

### 3. Dashboard Statistics
**Request**: `GET /dashboard/stats`

**Response** (`HTTP 200 OK`):
```json
{
  "total_tasks": 20,
  "completed_tasks": 12,
  "pending_tasks": 5,
  "in_progress_tasks": 3,
  "completion_rate": 60.0
}
```

### 4. Error Response Example
**Response** (`HTTP 404 Not Found`):
```json
{
  "error": "Task not found",
  "status_code": 404
}
```

---

## Installation & Setup

### Prerequisites
- Python 3.11 or higher
- Git

### Installation Steps (Windows)

1. **Clone the repository**:
   ```cmd
   git clone https://github.com/USERNAME/smarttask-api.git
   cd smarttask-api
   ```

2. **Create virtual environment**:
   ```cmd
   python -m venv venv
   ```

3. **Activate virtual environment**:
   ```cmd
   venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```cmd
   pip install -r requirements.txt
   ```

---

## Running the Application

Start the development server with live reload:

```cmd
uvicorn app.main:app --reload
```

The server will launch at:
- **Base API**: `http://127.0.0.1:8000`
- **Health Check**: `http://127.0.0.1:8000/health`

---

## Interactive API Documentation

FastAPI automatically generates interactive documentation accessible in your browser:

- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

---

## Running Automated Tests

The project includes an automated test suite using `pytest` and `httpx`. Tests execute against a separate in-memory SQLite database (`sqlite:///:memory:`), ensuring that tests are isolated, reproducible, and do not corrupt development data.

Run the test suite:

```cmd
pytest -v
```

Output:
```text
tests/test_root.py::test_health_check PASSED
tests/test_create_task.py::test_create_task_success PASSED
...
tests/test_validation.py::test_invalid_due_date_format PASSED
```

---

## CI/CD Pipeline

The `.github/workflows/tests.yml` workflow automatically builds and tests the application on GitHub infrastructure for every commit and pull request.

- **Trigger**: `push` and `pull_request` to `main` branch.
- **Environment**: Ubuntu Latest, Python 3.11.
- **Commands executed**:
  - `pip install -r requirements.txt`
  - `pytest -v`

---

## Future Improvements

- [ ] **JWT Authentication**: Add user accounts, login endpoints, and password hashing with bcrypt.
- [ ] **Task Subtasks & Tags**: Allow adding nested checklist items and custom tags.
- [ ] **Email Notifications**: Send reminder emails for tasks due today or overdue.
- [ ] **Dockerization**: Provide a `Dockerfile` and `docker-compose.yml` for containerized deployment.

---

## Author & Internship Interview Showcase Notes

**Created by**: BCA Student Backend Portfolio Project

### Summary for Internship Interviews
> "SmartTask is a Task Management & Productivity REST API built with FastAPI, Python 3.11, SQLAlchemy, and Pydantic. I designed the database schema using SQLAlchemy ORM and SQLite, implemented data validation with Pydantic v2 enums, and created a modular routing architecture separating core task CRUD from analytics. The project features full pagination, query parameter filtering, custom exception handlers returning structured JSON errors, a pytest automated test suite with an in-memory test database, and GitHub Actions CI pipeline."
