"""Task data model for todo application."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional


class TaskStatus(str, Enum):
    """Task completion status."""

    PENDING = "pending"
    COMPLETED = "completed"


@dataclass(frozen=False, slots=True)
class Task:
    """
    Represents a single todo task.

    Attributes:
        id: Unique identifier (auto-assigned by storage)
        title: Task description (1-200 chars)
        status: Current completion state
        created_at: ISO 8601 timestamp (UTC)
        completed_at: Completion timestamp (ISO 8601, UTC)
    """

    id: int
    title: str
    status: TaskStatus = TaskStatus.PENDING
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    completed_at: Optional[str] = None

    def __post_init__(self) -> None:
        """Validate task invariants."""
        # Validate title length
        if not (1 <= len(self.title) <= 200):
            raise ValueError(
                f"Title must be 1-200 chars, got {len(self.title)}"
            )

        # Validate completed tasks must have completed_at
        if self.status == TaskStatus.COMPLETED and not self.completed_at:
            raise ValueError(
                "Completed tasks must have completed_at timestamp"
            )
