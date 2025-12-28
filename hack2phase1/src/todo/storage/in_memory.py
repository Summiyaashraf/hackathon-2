"""In-memory storage backend for todo application."""

from typing import Optional

from todo.models.task import Task


class InMemoryStorage:
    """
    Thread-unsafe in-memory task storage.

    Attributes:
        _tasks: Dict[int, Task] - O(1) lookup by ID
        _next_id: int - Monotonic counter for ID generation
    """

    def __init__(self) -> None:
        """Initialize empty storage with ID counter."""
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1

    def _generate_id(self) -> int:
        """Generate unique task ID (auto-increment)."""
        current_id = self._next_id
        self._next_id += 1
        return current_id

    def add(self, title: str) -> Task:
        """
        Add a new task to storage.

        Args:
            title: Task title (1-200 characters)

        Returns:
            Created Task object

        Raises:
            ValueError: If title is invalid
        """
        task_id = self._generate_id()
        task = Task(id=task_id, title=title)
        self._tasks[task_id] = task
        return task

    def get(self, task_id: int) -> Optional[Task]:
        """
        Get a task by ID.

        Args:
            task_id: Task identifier

        Returns:
            Task if found, None otherwise
        """
        return self._tasks.get(task_id)

    def update(self, task_id: int, **kwargs: object) -> Task:
        """
        Update a task's attributes.

        Args:
            task_id: Task identifier
            **kwargs: Attributes to update (status, completed_at, etc.)

        Returns:
            Updated Task object

        Raises:
            KeyError: If task does not exist
            ValueError: If update creates invalid state
        """
        if task_id not in self._tasks:
            raise KeyError(f"Task {task_id} not found")

        task = self._tasks[task_id]
        # Create new task with updated attributes
        updated_data = {
            "id": task.id,
            "title": task.title,
            "status": kwargs.get("status", task.status),
            "created_at": kwargs.get("created_at", task.created_at),
            "completed_at": kwargs.get("completed_at", task.completed_at),
        }
        updated_task = Task(**updated_data)  # type: ignore
        self._tasks[task_id] = updated_task
        return updated_task

    def delete(self, task_id: int) -> bool:
        """
        Delete a task by ID.

        Args:
            task_id: Task identifier

        Returns:
            True if deleted, False if task not found
        """
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def list_all(self) -> list[Task]:
        """
        Get all tasks.

        Returns:
            List of all Task objects in insertion order
        """
        return list(self._tasks.values())
