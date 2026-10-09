"""Pydantic schemas and validation models for SmartTask API."""

from enum import Enum
from typing import Optional, List
from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator


class PriorityEnum(str, Enum):
    """Allowed priority values."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class StatusEnum(str, Enum):
    """Allowed status values."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class CategoryEnum(str, Enum):
    """Allowed category values."""
    WORK = "Work"
    STUDY = "Study"
    PERSONAL = "Personal"
    PROJECT = "Project"


class TaskBase(BaseModel):
    """Base Pydantic schema for task attributes."""
    title: str = Field(..., min_length=1, max_length=100, description="Title of the task")
    description: Optional[str] = Field(None, description="Optional detailed description")
    category: CategoryEnum = Field(..., description="Allowed category: Work, Study, Personal, Project")
    priority: PriorityEnum = Field(..., description="Allowed priority: low, medium, high")
    status: Optional[StatusEnum] = Field(
        StatusEnum.PENDING, description="Allowed status: pending, in_progress, completed"
    )
    due_date: Optional[date] = Field(None, description="Due date in YYYY-MM-DD format")

    @field_validator("title")
    def title_must_not_be_empty(cls, v: str) -> str:
        stripped = v.strip()
        if not stripped:
            raise ValueError("Title cannot be empty or whitespace only")
        return stripped


class TaskCreate(TaskBase):
    """Schema for task creation request payload."""
    pass


class TaskUpdate(BaseModel):
    """Schema for updating an existing task."""
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    category: Optional[CategoryEnum] = None
    priority: Optional[PriorityEnum] = None
    status: Optional[StatusEnum] = None
    due_date: Optional[date] = None

    @field_validator("title")
    def title_must_not_be_empty(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            stripped = v.strip()
            if not stripped:
                raise ValueError("Title cannot be empty or whitespace only")
            return stripped
        return v


class TaskResponse(TaskBase):
    """Schema for task API response."""
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PaginatedTasksResponse(BaseModel):
    """Schema for paginated task list response."""
    total: int
    page: int
    limit: int
    total_pages: int
    tasks: List[TaskResponse]


class DashboardStatsResponse(BaseModel):
    """Schema for dashboard productivity stats."""
    total_tasks: int
    completed_tasks: int
    pending_tasks: int
    in_progress_tasks: int
    completion_rate: float


class PrioritySummaryResponse(BaseModel):
    """Schema for task count by priority."""
    low: int
    medium: int
    high: int


class CategorySummaryResponse(BaseModel):
    """Schema for task count by category."""
    Work: int
    Study: int
    Personal: int
    Project: int


class HealthCheckResponse(BaseModel):
    """Schema for API health status."""
    status: str
    service: str


class ErrorResponse(BaseModel):
    """Schema for consistent error response structure."""
    error: str
    status_code: int
