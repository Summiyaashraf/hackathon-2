---
id: 002
title: Fix login content-type and disable auth guard
stage: misc
date: 2026-02-08
surface: agent
model: claude-haiku-4-5
feature: 001-todo-crud-features
branch: 001-todo-crud-features
user: ABC
command: /sp.implement
labels: ["authentication", "bugfix", "testing"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - frontend/src/services/api.ts
  - frontend/src/pages/Dashboard.tsx
tests:
  - none
---

## Prompt

Stop everything. I think the issue is that FastAPI expects content-type: application/x-www-form-urlencoded for login. Rewrite the login function in api.ts to use URLSearchParams. Also, for testing purposes, temporarily disable the Auth Guard in dashboard.tsx so I can at least see the UI you built.

## Response snapshot

Fixed two critical issues for testing the login functionality:

1. **Updated login function in api.ts (lines 69-92)**:
   - Changed from FormData to URLSearchParams
   - Set Content-Type header to 'application/x-www-form-urlencoded'
   - Changed field name from 'email' to 'username' (FastAPI OAuth2PasswordRequestForm expects 'username')
   - This now matches FastAPI's OAuth2PasswordRequestForm requirements

2. **Disabled Auth Guard in Dashboard.tsx (lines 261-263)**:
   - Commented out withAuthGuard(Dashboard) wrapper
   - Exported Dashboard component directly
   - Added comment indicating this is temporary for testing

These changes allow testing the login functionality with correct content type and accessing the Dashboard UI without authentication blocking.

## Outcome

- ✅ Impact: Fixed login API call to match FastAPI OAuth2 expectations; enabled direct Dashboard access for UI testing
- 🧪 Tests: No automated tests run; manual testing required
- 📁 Files: Modified 2 files (api.ts, Dashboard.tsx)
- 🔁 Next prompts: Test login functionality; re-enable Auth Guard after testing
- 🧠 Reflection: Quick fix addressing content-type mismatch and temporary auth bypass for development testing

## Evaluation notes (flywheel)

- Failure modes observed: FormData vs URLSearchParams content-type mismatch with FastAPI OAuth2
- Graders run and results (PASS/FAIL): N/A - manual testing required
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Test login with correct credentials; verify Dashboard renders correctly
