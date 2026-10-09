"""API router for Productivity Dashboard statistics and metrics."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get(
    "/stats",
    response_model=schemas.DashboardStatsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get overall productivity statistics",
    description="Returns aggregate counts of total, completed, pending, and in-progress tasks along with completion rate percentage.",
)
def get_dashboard_stats(db: Session = Depends(get_db)):
    return crud.get_dashboard_stats(db=db)


@router.get(
    "/priority-summary",
    response_model=schemas.PrioritySummaryResponse,
    status_code=status.HTTP_200_OK,
    summary="Get task breakdown by priority",
    description="Returns the total number of low, medium, and high priority tasks.",
)
def get_priority_summary(db: Session = Depends(get_db)):
    return crud.get_priority_summary(db=db)


@router.get(
    "/category-summary",
    response_model=schemas.CategorySummaryResponse,
    status_code=status.HTTP_200_OK,
    summary="Get task breakdown by category",
    description="Returns task counts categorized under Work, Study, Personal, and Project.",
)
def get_category_summary(db: Session = Depends(get_db)):
    return crud.get_category_summary(db=db)
