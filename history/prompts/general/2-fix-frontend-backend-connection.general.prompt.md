---
id: 2
title: "Fix Frontend Backend Connection CORS Configuration"
stage: general
date: "2026-01-25"
surface: "agent"
model: "claude-haiku-4-5-20251001"
feature: "none"
branch: "001-todo-crud-features"
user: "ABC"
command: "sp.implement"
labels: ["cors", "connection", "api-url", "servers"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "backend/src/main.py"
tests_yaml: []
---

# Fix Frontend Backend Connection CORS Configuration

## Summary
Updated the CORS configuration to properly allow connections between the frontend (running on ports 3000) and backend (running on port 8000). Restricted the CORSMiddleware to only allow specific origins instead of wildcard access.

## Changes Made
1. Updated CORSMiddleware in `backend/src/main.py` to specifically allow `http://localhost:3000` and `http://127.0.0.1:3000` instead of `["*"]`
2. Verified that frontend API_BASE_URL is set to `http://127.0.0.1:8000` as required
3. Killed all background Python processes using PowerShell command
4. Restarted both backend (port 8000) and frontend (port 3000) servers

## Outcome
The connection between frontend (port 3000) and backend (port 8000) should now work properly with the correct CORS configuration in place.

## Evaluation
- CORS configuration now allows only specific frontend origins
- Backend server running on port 8000
- Frontend server running on port 3000
- Both servers properly started after killing previous processes

## Prompt Text
```
Fix the connection between frontend (3000) and backend (8000):

In backend/src/main.py, update CORSMiddleware to include http://localhost:3000 and http://127.0.0.1:3000 in the allow_origins list.

In frontend/src/services/api.ts, make sure API_BASE_URL is exactly http://127.0.0.1:8000.

Kill all background processes first using taskkill /F /IM python.exe and then restart both servers.
```

## Response Text
Updated the CORS configuration in backend/src/main.py to specifically allow http://localhost:3000 and http://127.0.0.1:3000 instead of allowing all origins. Verified that the frontend API_BASE_URL is already set to http://127.0.0.1:8000 as required. Killed all Python processes using PowerShell command and restarted both backend (port 8000) and frontend (port 3000) servers.