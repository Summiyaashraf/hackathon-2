---
id: "007"
title: "Lifespan Handler and Port Fix"
stage: "general"
date_iso: "2026-01-22"
surface: "agent"
model: "claude-haiku-4-5-20251001"
feature: "none"
branch: "001-todo-crud-features"
user: "ABC"
command: "/sp.implement My backend failed to start with Error 10048 (Address already in use). Also, I see a DeprecationWarning for on_event."
labels:
  - "backend"
  - "fastapi"
  - "lifespan"
  - "port"
  - "cors"
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "backend/src/main.py"
tests_yaml: []
---

# Lifespan Handler and Port Fix

## PROMPT_TEXT

My backend failed to start with Error 10048 (Address already in use). Also, I see a DeprecationWarning for on_event.

Please update backend/src/main.py to:

Use the new Lifespan event handler instead of @app.on_event('startup').

Ensure the CORS settings are strictly allowing http://localhost:3000.

Provide a command to kill any process currently running on Port 8000 so I can start fresh.

## RESPONSE_TEXT

I've updated the backend/src/main.py file to use the new lifespan event handler and provided commands to kill processes on port 8000:

### Updated backend/src/main.py:
```python
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
    description="API for managing todo tasks",
    version="1.0.0",
    lifespan=lifespan
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

### Commands to kill processes running on Port 8000:

On Windows:
```bash
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F
```

Or use PowerShell:
```powershell
Get-NetTCPConnection -LocalPort 8000 | Select-Object OwningProcess
Stop-Process -Id <PROCESS_ID> -Force
```

On Linux/Mac:
```bash
lsof -i :8000
kill -9 $(lsof -t -i:8000)
```

Or alternatively:
```bash
sudo fuser -k 8000/tcp
```

The changes made:
1. Replaced deprecated @app.on_event("startup") with the modern lifespan event handler
2. Maintained strict CORS settings allowing only http://localhost:3000
3. Provided commands to resolve the "Address already in use" error

## OUTCOME

Updated the backend to use the modern lifespan event handler and provided commands to kill processes on port 8000.