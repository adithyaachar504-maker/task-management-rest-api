"""SQLAlchemy ORM models for SmartTask API."""

import datetime
from sqlalchemy import Column, Integer, String, Text, Date, DateTime
from app.database import Base


class Task(Base):
    """Task database model representing a productivity task item."""

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(20), nullable=False)
    priority = Column(String(10), nullable=False)
    status = Column(String(20), nullable=False, default="pending")
    due_date = Column(Date, nullable=True)
    created_at = Column(
        DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc), nullable=False
    )
    updated_at = Column(
        DateTime,
        default=lambda: datetime.datetime.now(datetime.timezone.utc),
        onupdate=lambda: datetime.datetime.now(datetime.timezone.utc),
        nullable=False,
    )
