"""Main entry point for todo application."""

from todo.models.task import TaskStatus
from todo.operations import NotFoundError, TaskOperations, ValidationError
from todo.storage.in_memory import InMemoryStorage
from todo.ui.display import print_tasks
from todo.ui.menu import (
    display_menu,
    get_task_id,
    get_task_title,
    get_user_choice,
)


def main() -> None:
    """Run the main application loop."""
    storage = InMemoryStorage()
    operations = TaskOperations(storage)

    print("\nWelcome to Todo App!")

    while True:
        display_menu()
        choice = get_user_choice()

        try:
            if choice == "0":
                print("\nGoodbye!")
                break
            elif choice == "1":
                _handle_add_task(operations)
            elif choice == "2":
                _handle_view_all(operations)
            elif choice == "3":
                _handle_view_pending(operations)
            elif choice == "4":
                _handle_view_completed(operations)
            elif choice == "5":
                _handle_mark_complete(operations)
            elif choice == "6":
                _handle_delete(operations)
            else:
                print("[ERROR] Invalid choice. Please enter 0-6.")
        except (ValidationError, NotFoundError) as e:
            print(f"[ERROR] {e}")
        except ValueError as e:
            print(f"[ERROR] Invalid input: {e}")
        except Exception as e:
            print(f"[ERROR] Unexpected error: {e}")


def _handle_add_task(operations: TaskOperations) -> None:
    """Handle add task operation."""
    title = get_task_title()
    task = operations.add_task(title)
    print(f"[OK] Task added: \"{task.title}\" (ID: {task.id})")


def _handle_view_all(operations: TaskOperations) -> None:
    """Handle view all tasks operation."""
    tasks = operations.list_tasks()
    print_tasks(tasks, title="All Tasks")


def _handle_view_pending(operations: TaskOperations) -> None:
    """Handle view pending tasks operation."""
    tasks = operations.filter_by_status(TaskStatus.PENDING)
    print_tasks(tasks, title="Pending Tasks")


def _handle_view_completed(operations: TaskOperations) -> None:
    """Handle view completed tasks operation."""
    tasks = operations.filter_by_status(TaskStatus.COMPLETED)
    print_tasks(tasks, title="Completed Tasks")


def _handle_mark_complete(operations: TaskOperations) -> None:
    """Handle mark task complete operation."""
    task_id = get_task_id()
    task = operations.mark_complete(task_id)
    print(f"[OK] Task marked complete: \"{task.title}\" (ID: {task.id})")


def _handle_delete(operations: TaskOperations) -> None:
    """Handle delete task operation."""
    task_id = get_task_id()
    operations.delete_task(task_id)
    print(f"[OK] Task deleted (ID: {task_id})")


if __name__ == "__main__":
    main()
