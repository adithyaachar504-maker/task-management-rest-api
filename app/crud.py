"""CRUD (Create, Read, Update, Delete) database operations for SmartTask API."""

import math
from enum import Enum
from datetime import date, datetime, timezone
from typing import Optional, List, Tuple
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app import models, schemas


def create_task(db: Session, task: schemas.TaskCreate) -> models.Task:
    """Create a new task in the database."""
    category_val = task.category.value if isinstance(task.category, Enum) else task.category
    priority_val = task.priority.value if isinstance(task.priority, Enum) else task.priority
    status_val = task.status.value if isinstance(task.status, Enum) else task.status

    db_task = models.Task(
        title=task.title,
        description=task.description,
        category=category_val,
        priority=priority_val,
        status=status_val,
        due_date=task.due_date,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_task_by_id(db: Session, task_id: int) -> Optional[models.Task]:
    """Retrieve a single task by its primary key ID."""
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def get_tasks(
    db: Session,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    category: Optional[str] = None,
    search: Optional[str] = None,
    page: int = 1,
    limit: int = 10,
) -> Tuple[List[models.Task], int, int]:
    """
    Retrieve tasks with optional status, priority, category filtering,
    case-insensitive search, and pagination.
    Returns (tasks_list, total_count, total_pages).
    """
    query = db.query(models.Task)

    if status:
        query = query.filter(models.Task.status == status)
    if priority:
        query = query.filter(models.Task.priority == priority)
    if category:
        query = query.filter(models.Task.category == category)
    if search:
        search_pattern = f"%{search.strip()}%"
        query = query.filter(
            or_(
                models.Task.title.ilike(search_pattern),
                models.Task.description.ilike(search_pattern),
            )
        )

    total = query.count()
    total_pages = math.ceil(total / limit) if total > 0 else 1
    offset = (page - 1) * limit
    tasks = (
        query.order_by(models.Task.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return tasks, total, total_pages


def update_task(
    db: Session, task_id: int, task_update: schemas.TaskUpdate
) -> Optional[models.Task]:
    """Update fields of an existing task."""
    db_task = get_task_by_id(db, task_id)
    if not db_task:
        return None

    update_data = task_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if value is not None:
            if isinstance(value, Enum):
                value = value.value
            setattr(db_task, key, value)

    db_task.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(db_task)
    return db_task


def complete_task(db: Session, task_id: int) -> Optional[models.Task]:
    """Mark a task as completed."""
    db_task = get_task_by_id(db, task_id)
    if not db_task:
        return None

    db_task.status = "completed"
    db_task.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int) -> bool:
    """Delete a task by ID."""
    db_task = get_task_by_id(db, task_id)
    if not db_task:
        return False

    db.delete(db_task)
    db.commit()
    return True


def get_overdue_tasks(db: Session) -> List[models.Task]:
    """Retrieve tasks whose due date has passed and status is not completed."""
    today = date.today()
    return (
        db.query(models.Task)
        .filter(models.Task.due_date < today)
        .filter(models.Task.status != "completed")
        .order_by(models.Task.due_date.asc())
        .all()
    )


def get_today_tasks(db: Session) -> List[models.Task]:
    """Retrieve tasks that are due today."""
    today = date.today()
    return (
        db.query(models.Task)
        .filter(models.Task.due_date == today)
        .order_by(models.Task.id.asc())
        .all()
    )


def get_dashboard_stats(db: Session) -> schemas.DashboardStatsResponse:
    """Calculate aggregate task statistics and completion rate."""
    total_tasks = db.query(models.Task).count()
    completed_tasks = (
        db.query(models.Task).filter(models.Task.status == "completed").count()
    )
    pending_tasks = (
        db.query(models.Task).filter(models.Task.status == "pending").count()
    )
    in_progress_tasks = (
        db.query(models.Task).filter(models.Task.status == "in_progress").count()
    )

    completion_rate = (
        round((completed_tasks / total_tasks) * 100, 2) if total_tasks > 0 else 0.0
    )

    return schemas.DashboardStatsResponse(
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks,
        in_progress_tasks=in_progress_tasks,
        completion_rate=completion_rate,
    )


def get_priority_summary(db: Session) -> schemas.PrioritySummaryResponse:
    """Calculate task counts grouped by priority."""
    low = db.query(models.Task).filter(models.Task.priority == "low").count()
    medium = db.query(models.Task).filter(models.Task.priority == "medium").count()
    high = db.query(models.Task).filter(models.Task.priority == "high").count()

    return schemas.PrioritySummaryResponse(low=low, medium=medium, high=high)


def get_category_summary(db: Session) -> schemas.CategorySummaryResponse:
    """Calculate task counts grouped by category."""
    work = db.query(models.Task).filter(models.Task.category == "Work").count()
    study = db.query(models.Task).filter(models.Task.category == "Study").count()
    personal = (
        db.query(models.Task).filter(models.Task.category == "Personal").count()
    )
    project = db.query(models.Task).filter(models.Task.category == "Project").count()

    return schemas.CategorySummaryResponse(
        Work=work, Study=study, Personal=personal, Project=project
    )
