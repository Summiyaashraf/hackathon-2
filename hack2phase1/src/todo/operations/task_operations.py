"""Business logic operations for todo application."""

from datetime import datetime, timezone

from todo.models.task import Task, TaskStatus
from todo.storage.in_memory import InMemoryStorage

from .exceptions import NotFoundError, ValidationError


class TaskOperations:
    """
    Orchestrates todo operations using storage and models.

    Encapsulates business logic for adding, updating, deleting, and querying tasks.
    """

    def __init__(self, storage: InMemoryStorage) -> None:
        """
        Initialize operations with a storage backend.

        Args:
            storage: InMemoryStorage instance
        """
        self._storage = storage

    def add_task(self, title: str) -> Task:
        """
        Add a new task with validation.

        Args:
            title: Task title (1-200 characters)

        Returns:
            Created Task object

        Raises:
            ValidationError: If title is invalid
        """
        title_stripped = title.strip()
        if not title_stripped:
            raise ValidationError("Title cannot be empty")
        if len(title_stripped) > 200:
            raise ValidationError("Title must not exceed 200 characters")

        task = self._storage.add(title_stripped)
        return task

    def list_tasks(self) -> list[Task]:
        """
        Get all tasks.

        Returns:
            List of all Task objects
        """
        return self._storage.list_all()

    def mark_complete(self, task_id: int) -> Task:
        """
        Mark a task as completed.

        Args:
            task_id: Task identifier

        Returns:
            Updated Task object

        Raises:
            NotFoundError: If task does not exist
        """
        task = self._storage.get(task_id)
        if task is None:
            raise NotFoundError(f"Task not found: ID {task_id}")

        if task.status == TaskStatus.COMPLETED:
            # Task already completed, return it
            return task

        now = datetime.now(timezone.utc).isoformat()
        updated_task = self._storage.update(
            task_id, status=TaskStatus.COMPLETED, completed_at=now
        )
        return updated_task

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by ID.

        Args:
            task_id: Task identifier

        Returns:
            True if deleted, False if task not found

        Raises:
            NotFoundError: If task does not exist
        """
        task = self._storage.get(task_id)
        if task is None:
            raise NotFoundError(f"Task not found: ID {task_id}")

        return self._storage.delete(task_id)

    def filter_by_status(self, status: TaskStatus) -> list[Task]:
        """
        Get tasks filtered by status.

        Args:
            status: TaskStatus to filter by

        Returns:
            List of Task objects with matching status
        """
        all_tasks = self._storage.list_all()
        return [task for task in all_tasks if task.status == status]
