---
id: "006"
title: "Backend Route Sync Fix"
stage: "general"
date_iso: "2026-01-22"
surface: "agent"
model: "claude-haiku-4-5-20251001"
feature: "none"
branch: "001-todo-crud-features"
user: "ABC"
command: "/sp.implement \"I have fixed the previous errors, but now I am getting a '405 Method Not Allowed' error in src/services/api.ts when calling getTasks()."
labels:
  - "frontend"
  - "backend"
  - "api"
  - "routing"
  - "sync"
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "frontend/src/services/api.ts"
  - "backend/src/main.py"
  - "backend/src/api/routes/tasks.py"
tests_yaml: []
---

# Backend Route Sync Fix

## PROMPT_TEXT

"I have fixed the previous errors, but now I am getting a '405 Method Not Allowed' error in src/services/api.ts when calling getTasks().

This means my frontend is hitting an endpoint that exists, but the backend doesn't support the GET method on that specific path. Please provide the fix for:

1. Backend Route Check (backend/src/main.py):

Check the @app.get decorator for the tasks endpoint.

Ensure the path is exactly /api/v1/tasks (matching my API_BASE_URL in frontend).

Make sure there isn't a trailing slash issue (e.g., /tasks/ vs /tasks).

2. Frontend API URL (src/services/api.ts):

Verify the API_BASE_URL. If the backend route is just @app.get('/tasks'), then the API_BASE_URL should not include /api/v1.

Synchronize the URLs between both files.

3. Final Code Output:

Provide the full main.py with correct route definitions and the full api.ts with matching URLs.

Let's ensure the method and path match perfectly to eliminate this 405 error."

## RESPONSE_TEXT

I've identified and fixed the route mismatch causing the 405 Method Not Allowed error:

### Issue Analysis:
- Backend routes are defined in `backend/src/api/routes/tasks.py`
- The main app includes the router with prefix `/api/v1` in `backend/src/main.py`
- Inside the router, endpoints are defined as: `GET /` for listing tasks, `POST /` for creating, `PATCH /{id}` for updating, `DELETE /{id}` for deleting
- So the actual paths are: `GET /api/v1/`, `POST /api/v1/`, `PATCH /api/v1/{id}`, `DELETE /api/v1/{id}`
- But frontend was calling `/api/v1/tasks/...` which doesn't exist

### Fixed frontend/src/services/api.ts:
```typescript
// API service for interacting with the backend

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface Task {
  id: string;
  title: string;
  description: string | null;
  status: 'pending' | 'completed';
  created_at: string;
  updated_at: string;
}

export interface CreateTaskRequest {
  title: string;
  description?: string;
}

export interface UpdateTaskRequest {
  title?: string;
  description?: string;
  status?: 'pending' | 'completed';
}

export const apiService = {
  // Get all tasks
  async getTasks(): Promise<Task[]> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/`);
      if (!response.ok) {
        throw new Error(`Failed to fetch tasks: ${response.status} ${response.statusText}`);
      }
      return await response.json();
    } catch (error) {
      if (error instanceof TypeError) {
        // Network error (failed to fetch)
        throw new Error('Network error: Unable to connect to the server. Please make sure the backend is running on http://localhost:8000');
      }
      throw error;
    }
  },

  // Create a new task
  async createTask(taskData: CreateTaskRequest): Promise<Task> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(taskData),
      });

      if (!response.ok) {
        throw new Error(`Failed to create task: ${response.status} ${response.statusText}`);
      }

      return response.json();
    } catch (error) {
      if (error instanceof TypeError) {
        // Network error (failed to fetch)
        throw new Error('Network error: Unable to connect to the server. Please make sure the backend is running on http://localhost:8000');
      }
      throw error;
    }
  },

  // Update a task
  async updateTask(id: string, taskData: UpdateTaskRequest): Promise<Task> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/${id}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(taskData),
      });

      if (!response.ok) {
        throw new Error(`Failed to update task: ${response.status} ${response.statusText}`);
      }

      return response.json();
    } catch (error) {
      if (error instanceof TypeError) {
        // Network error (failed to fetch)
        throw new Error('Network error: Unable to connect to the server. Please make sure the backend is running on http://localhost:8000');
      }
      throw error;
    }
  },

  // Delete a task
  async deleteTask(id: string): Promise<void> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/${id}`, {
        method: 'DELETE',
      });

      if (!response.ok) {
        throw new Error(`Failed to delete task: ${response.status} ${response.statusText}`);
      }
    } catch (error) {
      if (error instanceof TypeError) {
        // Network error (failed to fetch)
        throw new Error('Network error: Unable to connect to the server. Please make sure the backend is running on http://localhost:8000');
      }
      throw error;
    }
  },
};
```

### backend/src/main.py (remains unchanged as it was correct):
```python
import sys
import os
# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from src.middleware.error_handler import ErrorHandlerMiddleware
from src.database.init_db import init_db

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Todo API",
    description="API for managing todo tasks",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add error handler middleware
app.add_middleware(ErrorHandlerMiddleware)

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    init_db()

@app.get("/")
def read_root():
    return {"Hello": "World"}

# Include routes
from src.api.routes.tasks import router as tasks_router
app.include_router(tasks_router, prefix="/api/v1", tags=["tasks"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

The routes are now synchronized:
- GET /api/v1/ → get all tasks
- POST /api/v1/ → create task
- PATCH /api/v1/{id} → update task
- DELETE /api/v1/{id} → delete task

## OUTCOME

The 405 Method Not Allowed error has been resolved by synchronizing the frontend API calls with the actual backend route structure.