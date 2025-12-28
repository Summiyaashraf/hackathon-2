"""Unit tests for TaskOperations."""

import pytest

from todo.models.task import TaskStatus
from todo.operations.task_operations import TaskOperations
from todo.operations.exceptions import NotFoundError, ValidationError
from todo.storage.in_memory import InMemoryStorage


class TestTaskOperations:
    """Tests for business logic operations."""

    @pytest.fixture
    def operations(self) -> TaskOperations:
        """Create fresh TaskOperations instance for each test."""
        storage = InMemoryStorage()
        return TaskOperations(storage)

    def test_add_task_valid_title(self, operations: TaskOperations) -> None:
        """Test adding task with valid title."""
        task = operations.add_task("Buy milk")
        assert task.title == "Buy milk"
        assert task.status == TaskStatus.PENDING
        assert task.id > 0

    def test_add_task_strips_whitespace(self, operations: TaskOperations) -> None:
        """Test that whitespace is stripped from title."""
        task = operations.add_task("  Buy milk  ")
        assert task.title == "Buy milk"

    def test_add_task_empty_title_raises_error(self, operations: TaskOperations) -> None:
        """Test adding task with empty title raises ValidationError."""
        with pytest.raises(ValidationError, match="cannot be empty"):
            operations.add_task("")

    def test_add_task_whitespace_only_raises_error(
        self, operations: TaskOperations
    ) -> None:
        """Test adding task with whitespace-only title raises error."""
        with pytest.raises(ValidationError, match="cannot be empty"):
            operations.add_task("   ")

    def test_add_task_too_long_raises_error(self, operations: TaskOperations) -> None:
        """Test adding task with title > 200 chars raises error."""
        long_title = "a" * 201
        with pytest.raises(ValidationError, match="exceed 200"):
            operations.add_task(long_title)

    def test_mark_complete_existing_task(self, operations: TaskOperations) -> None:
        """Test marking existing task as complete."""
        task = operations.add_task("Task")
        marked = operations.mark_complete(task.id)
        assert marked.status == TaskStatus.COMPLETED
        assert marked.completed_at is not None

    def test_mark_complete_nonexistent_task(self, operations: TaskOperations) -> None:
        """Test marking non-existent task raises NotFoundError."""
        with pytest.raises(NotFoundError, match="not found"):
            operations.mark_complete(999)

    def test_mark_complete_already_completed(self, operations: TaskOperations) -> None:
        """Test marking already-completed task is idempotent."""
        task = operations.add_task("Task")
        marked_first = operations.mark_complete(task.id)
        marked_second = operations.mark_complete(task.id)
        assert marked_first.status == marked_second.status == TaskStatus.COMPLETED

    def test_delete_task_success(self, operations: TaskOperations) -> None:
        """Test deleting existing task."""
        task = operations.add_task("Task")
        result = operations.delete_task(task.id)
        assert result is True

    def test_delete_task_nonexistent(self, operations: TaskOperations) -> None:
        """Test deleting non-existent task raises NotFoundError."""
        with pytest.raises(NotFoundError, match="not found"):
            operations.delete_task(999)

    def test_list_tasks_empty(self, operations: TaskOperations) -> None:
        """Test listing tasks when empty."""
        tasks = operations.list_tasks()
        assert tasks == []

    def test_list_tasks_multiple(self, operations: TaskOperations) -> None:
        """Test listing multiple tasks."""
        operations.add_task("Task 1")
        operations.add_task("Task 2")
        operations.add_task("Task 3")
        tasks = operations.list_tasks()
        assert len(tasks) == 3

    def test_filter_by_status_pending(self, operations: TaskOperations) -> None:
        """Test filtering tasks by PENDING status."""
        operations.add_task("Pending 1")
        operations.add_task("Pending 2")
        task = operations.add_task("To complete")
        operations.mark_complete(task.id)

        pending = operations.filter_by_status(TaskStatus.PENDING)
        assert len(pending) == 2
        assert all(t.status == TaskStatus.PENDING for t in pending)

    def test_filter_by_status_completed(self, operations: TaskOperations) -> None:
        """Test filtering tasks by COMPLETED status."""
        task1 = operations.add_task("Task 1")
        task2 = operations.add_task("Task 2")
        operations.mark_complete(task1.id)

        completed = operations.filter_by_status(TaskStatus.COMPLETED)
        assert len(completed) == 1
        assert completed[0].status == TaskStatus.COMPLETED

    def test_filter_by_status_no_matches(self, operations: TaskOperations) -> None:
        """Test filtering when no tasks match."""
        operations.add_task("Pending task")
        completed = operations.filter_by_status(TaskStatus.COMPLETED)
        assert completed == []

    def test_full_task_lifecycle(self, operations: TaskOperations) -> None:
        """Test complete task lifecycle: add -> view -> mark complete -> delete."""
        # Add
        task = operations.add_task("Buy groceries")
        assert task.status == TaskStatus.PENDING

        # List
        tasks = operations.list_tasks()
        assert len(tasks) == 1

        # Mark complete
        completed = operations.mark_complete(task.id)
        assert completed.status == TaskStatus.COMPLETED

        # Delete
        result = operations.delete_task(task.id)
        assert result is True
        assert len(operations.list_tasks()) == 0
