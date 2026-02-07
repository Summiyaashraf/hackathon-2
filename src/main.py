import bcrypt
if not hasattr(bcrypt, "__about__"):
    bcrypt.__about__ = type('About', (), {'__version__': bcrypt.__version__})

import sys
import os
# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from src.middleware.error_handler import ErrorHandlerMiddleware
from src.database.init_db import init_db

# Load environment variables
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for startup and shutdown events."""
    # Startup
    init_db()
    yield
    # Shutdown (if needed)
    pass

app = FastAPI(
    title="Todo API",
    description="API for managing todo tasks with user authentication",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:3001", "http://127.0.0.1:3001"],  # Frontend origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add error handler middleware
app.add_middleware(ErrorHandlerMiddleware)

@app.get("/")
def read_root():
    return {"Hello": "World", "message": "Welcome to the Todo API with authentication"}

# Include routes - updated to use new authentication-based routes
from src.api.routes.auth import router as auth_router
from src.api.routes.tasks import router as tasks_router

# Authentication routes
app.include_router(auth_router, prefix="", tags=["auth"])

# Task routes - these now include user_id in the path and require authentication
# The routes are defined in the tasks router with the full path including /api/{user_id}/tasks
app.include_router(tasks_router, tags=["tasks"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)