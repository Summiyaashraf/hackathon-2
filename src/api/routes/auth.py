import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

import bcrypt
from fastapi import APIRouter, Depends, HTTPException, status, Form, Request
from sqlmodel import Session, select
from typing import Optional
from src.models.user_model import User, UserCreate, UserRead
from src.database.database import get_session
from src.middleware.jwt_auth import jwt_manager, JWTBearer, get_current_user_from_request
import uuid

router = APIRouter()


def get_password_hash(password: str):
    """Hash a plain password using direct bcrypt."""
    # Ensure password is truncated to 72 bytes and encoded to bytes
    pwd_bytes = password.encode('utf-8')[:72]
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode('utf-8')


def verify_password(plain_password: str, hashed_password: str):
    """Verify a plain password against a hashed password using direct bcrypt."""
    pwd_bytes = plain_password.encode('utf-8')[:72]
    return bcrypt.checkpw(pwd_bytes, hashed_password.encode('utf-8'))


@router.post("/auth/register", response_model=UserRead)
def register_user(user: UserCreate, session: Session = Depends(get_session)):
    """Register a new user."""
    # Check if user already exists
    existing_user = session.exec(select(User).where(User.email == user.email)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash the password
    password_hash = get_password_hash(user.password)

    # Create the user
    db_user = User(
        email=user.email,
        username=user.username,
        password_hash=password_hash
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.post("/auth/login")
def login_user(email: str = Form(...), password: str = Form(...), session: Session = Depends(get_session)):
    """Login a user and return JWT token."""
    # Find the user by email
    user = session.exec(select(User).where(User.email == email)).first()

    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user"
        )

    # Create access token
    access_token = jwt_manager.create_access_token(
        user_id=str(user.id),
        email=user.email
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": str(user.id),
            "email": user.email,
            "username": user.username
        }
    }


@router.get("/auth/me", response_model=UserRead)
def get_current_user_profile(
    request: Request,
    session: Session = Depends(get_session),
    token_data: dict = Depends(JWTBearer())
):
    """Get current user's profile information."""
    # The JWTBearer middleware sets the user_id in request.state
    current_user_id = request.state.user_id
    user = session.get(User, uuid.UUID(current_user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user