"""Display formatting functions for todo application."""

from todo.models.task import Task


def format_task(task: Task) -> str:
    """
    Format a task for display.

    Args:
        task: Task object to format

    Returns:
        Formatted task string
    """
    status_display = task.status.value.upper()
    created = task.created_at
    completed = (
        f"\n    Completed: {task.completed_at}" if task.completed_at else ""
    )

    return (
        f"[{task.id}] {task.title} [{status_display}]\n"
        f"    Created: {created}{completed}"
    )


def print_tasks(tasks: list[Task], title: str = "Tasks") -> None:
    """
    Print a list of tasks with a title.

    Args:
        tasks: List of Task objects to display
        title: Title to display above the list
    """
    print(f"\n{title}")
    print("=" * 50)

    if not tasks:
        print("No tasks found.")
        return

    for task in tasks:
        print(format_task(task))
        print()
