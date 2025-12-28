"""Unit tests for InMemoryStorage."""

import pytest

from todo.models.task import TaskStatus
from todo.storage.in_memory import InMemoryStorage


class TestStorageOperations:
    """Tests for storage CRUD operations."""

    def test_add_task_generates_id(self) -> None:
        """Test that add generates unique IDs."""
        storage = InMemoryStorage()
        task1 = storage.add("Task 1")
        task2 = storage.add("Task 2")
        assert task1.id == 1
        assert task2.id == 2

    def test_get_task_existing(self) -> None:
        """Test getting an existing task."""
        storage = InMemoryStorage()
        task = storage.add("Test task")
        retrieved = storage.get(task.id)
        assert retrieved is not None
        assert retrieved.title == "Test task"

    def test_get_task_nonexistent(self) -> None:
        """Test getting a non-existent task returns None."""
        storage = InMemoryStorage()
        result = storage.get(999)
        assert result is None

    def test_update_task_status(self) -> None:
        """Test updating task status with required timestamp."""
        storage = InMemoryStorage()
        task = storage.add("Task")
        timestamp = "2025-01-01T00:00:00+00:00"
        updated = storage.update(
            task.id,
            status=TaskStatus.COMPLETED,
            completed_at=timestamp,
        )
        assert updated.status == TaskStatus.COMPLETED
        assert updated.completed_at == timestamp

    def test_update_task_with_completed_at(self) -> None:
        """Test updating task with completed timestamp."""
        storage = InMemoryStorage()
        task = storage.add("Task")
        timestamp = "2025-01-01T00:00:00+00:00"
        updated = storage.update(
            task.id,
            status=TaskStatus.COMPLETED,
            completed_at=timestamp,
        )
        assert updated.completed_at == timestamp

    def test_delete_task_success(self) -> None:
        """Test deleting an existing task."""
        storage = InMemoryStorage()
        task = storage.add("Task")
        result = storage.delete(task.id)
        assert result is True
        assert storage.get(task.id) is None

    def test_delete_task_nonexistent(self) -> None:
        """Test deleting non-existent task returns False."""
        storage = InMemoryStorage()
        result = storage.delete(999)
        assert result is False

    def test_list_all_empty(self) -> None:
        """Test listing empty storage."""
        storage = InMemoryStorage()
        tasks = storage.list_all()
        assert tasks == []

    def test_list_all_multiple(self) -> None:
        """Test listing multiple tasks."""
        storage = InMemoryStorage()
        storage.add("Task 1")
        storage.add("Task 2")
        storage.add("Task 3")
        tasks = storage.list_all()
        assert len(tasks) == 3

    def test_update_nonexistent_raises_error(self) -> None:
        """Test updating non-existent task raises KeyError."""
        storage = InMemoryStorage()
        with pytest.raises(KeyError):
            storage.update(999, status=TaskStatus.COMPLETED)

    def test_id_generation_monotonic(self) -> None:
        """Test ID generation is monotonically increasing."""
        storage = InMemoryStorage()
        ids = []
        for i in range(10):
            task = storage.add(f"Task {i}")
            ids.append(task.id)

        # Verify IDs are sequential
        assert ids == list(range(1, 11))
        # Verify no gaps
        assert ids == sorted(ids)
