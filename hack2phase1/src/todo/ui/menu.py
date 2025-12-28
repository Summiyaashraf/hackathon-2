"""Menu system for todo application."""


def display_menu() -> None:
    """Display the main menu options."""
    print("\n" + "=" * 50)
    print("Todo App - Main Menu")
    print("=" * 50)
    print("1. Add Task")
    print("2. View All Tasks")
    print("3. View Pending Tasks")
    print("4. View Completed Tasks")
    print("5. Mark Task Complete")
    print("6. Delete Task")
    print("0. Exit")
    print("=" * 50)


def get_user_choice() -> str:
    """
    Get and validate user's menu choice.

    Returns:
        User's input (may need further validation)
    """
    choice = input("Enter choice: ").strip()
    return choice


def get_task_id() -> int:
    """
    Get a task ID from user input.

    Returns:
        Task ID as integer

    Raises:
        ValueError: If input is not a valid integer
    """
    task_id_str = input("Enter task ID: ").strip()
    return int(task_id_str)


def get_task_title() -> str:
    """
    Get a task title from user input.

    Returns:
        Task title string

    Raises:
        ValueError: If input is empty
    """
    title = input("Enter task title: ").strip()
    return title
