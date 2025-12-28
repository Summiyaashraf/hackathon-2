"""Unit tests for Task data model."""

import pytest

from todo.models.task import Task, TaskStatus


class TestTaskCreation:
    """Tests for Task creation and validation."""

    def test_task_creation_valid(self) -> None:
        """Test creating a valid task."""
        task = Task(id=1, title="Buy milk")
        assert task.id == 1
        assert task.title == "Buy milk"
        assert task.status == TaskStatus.PENDING
        assert task.created_at is not None
        assert task.completed_at is None

    def test_task_creation_with_completed_status(self) -> None:
        """Test creating a completed task with timestamp."""
        task = Task(
            id=1,
            title="Done task",
            status=TaskStatus.COMPLETED,
            completed_at="2025-01-01T00:00:00+00:00",
        )
        assert task.status == TaskStatus.COMPLETED
        assert task.completed_at == "2025-01-01T00:00:00+00:00"

    def test_task_validation_title_empty(self) -> None:
        """Test that empty title raises ValueError."""
        with pytest.raises(ValueError, match="1-200 chars"):
            Task(id=1, title="")

    def test_task_validation_title_too_long(self) -> None:
        """Test that title longer than 200 chars raises ValueError."""
        long_title = "a" * 201
        with pytest.raises(ValueError, match="1-200 chars"):
            Task(id=1, title=long_title)

    def test_task_validation_title_at_boundary(self) -> None:
        """Test title at exactly 200 characters."""
        exact_title = "a" * 200
        task = Task(id=1, title=exact_title)
        assert task.title == exact_title

    def test_status_enum_values(self) -> None:
        """Test that TaskStatus enum has expected values."""
        assert TaskStatus.PENDING.value == "pending"
        assert TaskStatus.COMPLETED.value == "completed"

    def test_completed_task_requires_timestamp(self) -> None:
        """Test that COMPLETED status without timestamp raises ValueError."""
        with pytest.raises(ValueError, match="Completed tasks must have"):
            Task(id=1, title="Task", status=TaskStatus.COMPLETED)

    def test_task_with_special_characters(self) -> None:
        """Test task title with special characters."""
        title = "Buy milk & bread (2x) @ store!"
        task = Task(id=1, title=title)
        assert task.title == title

    def test_task_str_representation(self) -> None:
        """Test task string representation."""
        task = Task(id=1, title="Test task")
        task_str = str(task)
        assert "Task" in task_str or "id" in task_str
