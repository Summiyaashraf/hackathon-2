"""Integration tests for todo application workflows."""

import pytest

from todo.models.task import TaskStatus
from todo.operations.task_operations import TaskOperations
from todo.storage.in_memory import InMemoryStorage


class TestWorkflows:
    """Tests for complete workflows across layers."""

    @pytest.fixture
    def operations(self) -> TaskOperations:
        """Create fresh operations instance."""
        storage = InMemoryStorage()
        return TaskOperations(storage)

    def test_full_task_lifecycle(self, operations: TaskOperations) -> None:
        """Test complete workflow: add -> view -> mark complete -> view -> delete."""
        # Add task
        task = operations.add_task("Buy groceries")
        task_id = task.id

        # View all
        all_tasks = operations.list_tasks()
        assert len(all_tasks) == 1
        assert all_tasks[0].title == "Buy groceries"

        # Mark complete
        marked = operations.mark_complete(task_id)
        assert marked.status == TaskStatus.COMPLETED

        # View completed
        completed = operations.filter_by_status(TaskStatus.COMPLETED)
        assert len(completed) == 1

        # Delete
        operations.delete_task(task_id)
        assert len(operations.list_tasks()) == 0

    def test_multiple_operations_independence(self, operations: TaskOperations) -> None:
        """Test that multiple operations don't interfere."""
        task1 = operations.add_task("Task 1")
        task2 = operations.add_task("Task 2")
        task3 = operations.add_task("Task 3")

        # Mark one complete
        operations.mark_complete(task2.id)

        # Verify others unchanged
        task1_check = operations._storage.get(task1.id)
        task3_check = operations._storage.get(task3.id)
        assert task1_check is not None
        assert task3_check is not None
        assert task1_check.status == TaskStatus.PENDING
        assert task3_check.status == TaskStatus.PENDING

        # Delete one
        operations.delete_task(task1.id)

        # Verify others still exist
        assert len(operations.list_tasks()) == 2

    def test_id_generation_monotonic(self, operations: TaskOperations) -> None:
        """Test that IDs are monotonically increasing across operations."""
        ids = []
        for i in range(10):
            task = operations.add_task(f"Task {i}")
            ids.append(task.id)

        assert ids == list(range(1, 11))

    def test_status_filter_correctness(self, operations: TaskOperations) -> None:
        """Test status filtering with mixed states."""
        # Add 10 tasks
        task_ids = []
        for i in range(10):
            task = operations.add_task(f"Task {i}")
            task_ids.append(task.id)

        # Mark every other one as complete
        for i in range(0, 10, 2):
            operations.mark_complete(task_ids[i])

        # Verify counts
        pending = operations.filter_by_status(TaskStatus.PENDING)
        completed = operations.filter_by_status(TaskStatus.COMPLETED)

        assert len(pending) == 5
        assert len(completed) == 5
        assert len(pending) + len(completed) == 10

    def test_error_handling_consistency(self, operations: TaskOperations) -> None:
        """Test that errors don't corrupt state."""
        task = operations.add_task("Task")

        # Try invalid operation
        try:
            operations.mark_complete(999)
        except Exception:
            pass

        # Verify original task still intact
        retrieved = operations._storage.get(task.id)
        assert retrieved is not None
        assert retrieved.status == TaskStatus.PENDING

    def test_concurrent_adds_and_deletes(self, operations: TaskOperations) -> None:
        """Test mix of add and delete operations."""
        # Add 5 tasks
        for i in range(5):
            operations.add_task(f"Task {i}")

        # Delete odd IDs
        operations.delete_task(1)
        operations.delete_task(3)
        operations.delete_task(5)

        # Verify remaining
        remaining = operations.list_tasks()
        assert len(remaining) == 2
        remaining_ids = {t.id for t in remaining}
        assert remaining_ids == {2, 4}

    def test_add_after_delete(self, operations: TaskOperations) -> None:
        """Test adding tasks after deleting."""
        task1 = operations.add_task("Task 1")
        task2 = operations.add_task("Task 2")

        # Delete first
        operations.delete_task(task1.id)

        # Add new
        task3 = operations.add_task("Task 3")

        # IDs should continue monotonically
        assert task3.id == 3
        assert len(operations.list_tasks()) == 2

    def test_whitespace_handling_across_layers(self, operations: TaskOperations) -> None:
        """Test whitespace is properly handled through all layers."""
        task = operations.add_task("  Task with spaces  ")
        retrieved = operations._storage.get(task.id)
        assert retrieved is not None
        assert retrieved.title == "Task with spaces"

    def test_large_title_acceptance(self, operations: TaskOperations) -> None:
        """Test task with maximum-length title."""
        max_title = "x" * 200
        task = operations.add_task(max_title)
        retrieved = operations._storage.get(task.id)
        assert retrieved is not None
        assert len(retrieved.title) == 200
