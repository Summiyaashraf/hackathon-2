"""Exception classes for todo application."""


class TodoAppError(Exception):
    """Base exception for todo app errors."""

    pass


class ValidationError(TodoAppError):
    """Invalid input or constraint violation."""

    pass


class NotFoundError(TodoAppError):
    """Requested resource does not exist."""

    pass
