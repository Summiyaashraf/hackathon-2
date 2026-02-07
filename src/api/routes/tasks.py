import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlmodel import Session
from typing import List, Optional
from src.models.task_model import Task, TaskCreate, TaskRead, TaskUpdate
from src.database.database import get_session
from src.services.task_service import (
    get_all_tasks_by_user,
    create_task as service_create_task,
    update_task as service_update_task,
    delete_task as service_delete_task,
    get_task_by_id_and_user
)
from src.middleware.jwt_auth import JWTBearer, get_current_user_from_request, require_same_user
import uuid

router = APIRouter()

@router.get("/api/{user_id}/tasks", response_model=List[TaskRead])
def get_tasks(
    request: Request,
    user_id: str,
    status: Optional[str] = Query(None, pattern=r"^(pending|completed)$"),
    limit: Optional[int] = Query(None, ge=1, le=100),
    offset: Optional[int] = Query(0, ge=0),
    session: Session = Depends(get_session),
    token_data: dict = Depends(JWTBearer())
):
    """
    Retrieve all tasks for the specified user.
    """
    # Verify that the user in the token matches the user in the path
    current_user_id = get_current_user_from_request(request)
    if str(current_user_id) != str(user_id):
        raise HTTPException(
            status_code=403,
            detail="Access forbidden: User does not have permission to access this resource"
        )

    tasks = get_all_tasks_by_user(session, user_id, status_filter=status, limit=limit, offset=offset)

    # Add pagination info if needed
    response = {
        "tasks": tasks,
        "pagination": {
            "total": len(tasks),  # In a real app, you'd get the total from the DB
            "limit": limit,
            "offset": offset
        }
    }

    return tasks

@router.post("/api/{user_id}/tasks", response_model=TaskRead, status_code=201)
def create_task_endpoint(
    request: Request,
    user_id: str,
    task: TaskCreate,
    session: Session = Depends(get_session),
    token_data: dict = Depends(JWTBearer())
):
    """
    Create a new task for the specified user.
    """
    # Verify that the user in the token matches the user in the path
    current_user_id = get_current_user_from_request(request)
    if str(current_user_id) != str(user_id):
        raise HTTPException(
            status_code=403,
            detail="Access forbidden: User does not have permission to access this resource"
        )

    # Create task with the user_id from the path/token
    db_task = service_create_task(session, task, user_id)
    return db_task

@router.get("/api/{user_id}/tasks/{task_id}", response_model=TaskRead)
def get_single_task(
    request: Request,
    user_id: str,
    task_id: str,
    session: Session = Depends(get_session),
    token_data: dict = Depends(JWTBearer())
):
    """
    Retrieve a specific task for the specified user.
    """
    # Verify that the user in the token matches the user in the path
    current_user_id = get_current_user_from_request(request)
    if str(current_user_id) != str(user_id):
        raise HTTPException(
            status_code=403,
            detail="Access forbidden: User does not have permission to access this resource"
        )

    # Validate UUID format
    try:
        uuid.UUID(task_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid task ID format")

    db_task = get_task_by_id_and_user(session, task_id, user_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    return db_task

@router.patch("/api/{user_id}/tasks/{task_id}", response_model=TaskRead)
def update_task_endpoint(
    request: Request,
    user_id: str,
    task_id: str,
    task_update: TaskUpdate,
    session: Session = Depends(get_session),
    token_data: dict = Depends(JWTBearer())
):
    """
    Update an existing task for the specified user.
    """
    # Verify that the user in the token matches the user in the path
    current_user_id = get_current_user_from_request(request)
    if str(current_user_id) != str(user_id):
        raise HTTPException(
            status_code=403,
            detail="Access forbidden: User does not have permission to access this resource"
        )

    # Validate UUID format
    try:
        uuid.UUID(task_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid task ID format")

    db_task = service_update_task(session, task_id, task_update, user_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    return db_task

@router.delete("/api/{user_id}/tasks/{task_id}")
def delete_task_endpoint(
    request: Request,
    user_id: str,
    task_id: str,
    session: Session = Depends(get_session),
    token_data: dict = Depends(JWTBearer())
):
    """
    Delete a task for the specified user.
    """
    # Verify that the user in the token matches the user in the path
    current_user_id = get_current_user_from_request(request)
    if str(current_user_id) != str(user_id):
        raise HTTPException(
            status_code=403,
            detail="Access forbidden: User does not have permission to access this resource"
        )

    # Validate UUID format
    try:
        uuid.UUID(task_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid task ID format")

    success = service_delete_task(session, task_id, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"message": "Task deleted successfully"}