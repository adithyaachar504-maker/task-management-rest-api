"""API router for Task management operations."""

from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post(
    "",
    response_model=schemas.TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    description="Create a task with title, description, category, priority, status, and due_date.",
)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
):
    return crud.create_task(db=db, task=task)


@router.get(
    "",
    response_model=schemas.PaginatedTasksResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve all tasks with filtering, search, and pagination",
    description="List tasks with optional filters for status, priority, category, keyword search, and pagination.",
)
def get_tasks(
    status: Optional[schemas.StatusEnum] = Query(None, description="Filter by status"),
    priority: Optional[schemas.PriorityEnum] = Query(None, description="Filter by priority"),
    category: Optional[schemas.CategoryEnum] = Query(None, description="Filter by category"),
    search: Optional[str] = Query(None, description="Search keyword in title or description"),
    page: int = Query(1, ge=1, description="Page number (1-based)"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
):
    status_val = status.value if status else None
    priority_val = priority.value if priority else None
    category_val = category.value if category else None

    tasks, total, total_pages = crud.get_tasks(
        db=db,
        status=status_val,
        priority=priority_val,
        category=category_val,
        search=search,
        page=page,
        limit=limit,
    )

    return schemas.PaginatedTasksResponse(
        total=total,
        page=page,
        limit=limit,
        total_pages=total_pages,
        tasks=tasks,
    )


@router.get(
    "/overdue",
    response_model=List[schemas.TaskResponse],
    status_code=status.HTTP_200_OK,
    summary="Retrieve overdue tasks",
    description="Fetch tasks whose due date has passed and are not marked as completed.",
)
def get_overdue_tasks(db: Session = Depends(get_db)):
    return crud.get_overdue_tasks(db=db)


@router.get(
    "/today",
    response_model=List[schemas.TaskResponse],
    status_code=status.HTTP_200_OK,
    summary="Retrieve tasks due today",
    description="Fetch tasks whose due date is equal to today's date.",
)
def get_today_tasks(db: Session = Depends(get_db)):
    return crud.get_today_tasks(db=db)


@router.get(
    "/{task_id}",
    response_model=schemas.TaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Get task by ID",
    description="Retrieve details of a single task by its unique identifier.",
)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = crud.get_task_by_id(db=db, task_id=task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return task


@router.put(
    "/{task_id}",
    response_model=schemas.TaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Update a task",
    description="Update the details of an existing task.",
)
def update_task(
    task_id: int,
    task_update: schemas.TaskUpdate,
    db: Session = Depends(get_db),
):
    updated_task = crud.update_task(db=db, task_id=task_id, task_update=task_update)
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return updated_task


@router.patch(
    "/{task_id}/complete",
    response_model=schemas.TaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Mark task as completed",
    description="Quick action endpoint to change task status to completed.",
)
def complete_task(task_id: int, db: Session = Depends(get_db)):
    completed_task = crud.complete_task(db=db, task_id=task_id)
    if not completed_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return completed_task


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
    description="Permanently remove a task from the database.",
)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_task(db=db, task_id=task_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return None
