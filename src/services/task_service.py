import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sqlmodel import Session, select
from typing import List, Optional
from src.models.task_model import Task, TaskCreate, TaskUpdate
import uuid

def get_all_tasks(session: Session) -> List[Task]:
    """Get all tasks (legacy function)."""
    tasks = session.exec(select(Task)).all()
    return tasks

def get_all_tasks_by_user(session: Session, user_id: str, status_filter: Optional[str] = None, limit: Optional[int] = None, offset: Optional[int] = 0) -> List[Task]:
    """Get all tasks for a specific user with optional filtering."""
    statement = select(Task).where(Task.user_id == user_id)

    if status_filter:
        statement = statement.where(Task.status == status_filter)

    if limit:
        statement = statement.limit(limit)

    if offset:
        statement = statement.offset(offset)

    tasks = session.exec(statement).all()
    return tasks

def get_task_by_id(session: Session, task_id: str) -> Optional[Task]:
    """Get a task by ID (legacy function)."""
    task = session.get(Task, task_id)
    return task

def get_task_by_id_and_user(session: Session, task_id: str, user_id: str) -> Optional[Task]:
    """Get a task by ID and user ID to ensure user owns the task."""
    # Validate UUID format
    try:
        uuid_task_id = uuid.UUID(task_id)
        uuid_user_id = uuid.UUID(user_id)
    except ValueError:
        return None

    statement = select(Task).where(Task.id == uuid_task_id, Task.user_id == uuid_user_id)
    task = session.exec(statement).first()
    return task

def create_task(session: Session, task_create: TaskCreate, user_id: str) -> Task:
    """Create a new task for a specific user."""
    # Validate UUID format
    try:
        uuid_user_id = uuid.UUID(user_id)
    except ValueError:
        raise ValueError("Invalid user ID format")

    db_task = Task.model_validate(task_create.model_dump())
    db_task.user_id = uuid_user_id  # Set the user_id from the parameter
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

def update_task(session: Session, task_id: str, task_update: TaskUpdate, user_id: str) -> Optional[Task]:
    """Update an existing task for a specific user."""
    # Validate UUID format
    try:
        uuid_task_id = uuid.UUID(task_id)
        uuid_user_id = uuid.UUID(user_id)
    except ValueError:
        return None

    statement = select(Task).where(Task.id == uuid_task_id, Task.user_id == uuid_user_id)
    db_task = session.exec(statement).first()

    if not db_task:
        return None

    # Update only the fields that are provided
    update_data = task_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)

    # Update the updated_at timestamp
    from datetime import datetime
    db_task.updated_at = datetime.utcnow()

    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

def delete_task(session: Session, task_id: str, user_id: str) -> bool:
    """Delete a task for a specific user."""
    # Validate UUID format
    try:
        uuid_task_id = uuid.UUID(task_id)
        uuid_user_id = uuid.UUID(user_id)
    except ValueError:
        return False

    statement = select(Task).where(Task.id == uuid_task_id, Task.user_id == uuid_user_id)
    db_task = session.exec(statement).first()

    if not db_task:
        return False

    session.delete(db_task)
    session.commit()
    return True