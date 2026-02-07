# Quickstart Guide: Todo Application

## Prerequisites
- Python 3.11+
- Node.js 18+
- Neon DB account and connection string

## Setup Instructions

### Backend Setup
1. Navigate to the backend directory: `cd backend`
2. Install Python dependencies: `pip install -r requirements.txt`
3. Create a `.env` file in the backend directory with the following variables:
   ```
   NEON_DB_URL=your_neon_db_connection_string
   BETTER_AUTH_SECRET=your_jwt_secret_key_here
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   DEBUG=true
   ```
4. Initialize the database (tables will be created automatically on first run)
5. Start the server: `python run_server.py` or `uvicorn src.main:app --reload --port 8080`

### Frontend Setup
1. Navigate to the frontend directory: `cd frontend`
2. Install dependencies: `npm install`
3. Create a `.env.local` file in the frontend directory:
   ```
   NEXT_PUBLIC_API_URL=http://127.0.0.1:8080
   ```
4. Start the development server: `npm run dev`
5. Open your browser to `http://localhost:3000`

## First Time Usage

### 1. Register a New Account
- Navigate to `http://localhost:3000/auth/register`
- Enter your email, optional username, and password (minimum 8 characters)
- Click "Sign Up" - you'll be automatically logged in and redirected to the dashboard

### 2. Login
- Navigate to `http://localhost:3000/auth/login`
- Enter your email and password
- Click "Sign In" to access your dashboard

### 3. Using the Dashboard
- **Create Tasks**: Click the "New Task" button to create a new task
- **Toggle Status**: Click the checkbox to mark tasks as completed/pending
- **Edit Tasks**: Click the edit icon to modify task title or description
- **Delete Tasks**: Click the trash icon to remove tasks
- **Filter Tasks**: Use the filter buttons (All, Pending, Completed) to view specific tasks
- **Dark Mode**: Click the theme toggle button in the header to switch between light and dark modes

## API Endpoints

### Authentication Endpoints
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and receive JWT token
- `GET /auth/me` - Get current user profile (requires authentication)

### Task Endpoints (All require authentication)
- `GET /api/{user_id}/tasks` - Get all tasks for the authenticated user
- `POST /api/{user_id}/tasks` - Create a new task
- `GET /api/{user_id}/tasks/{task_id}` - Get a specific task
- `PATCH /api/{user_id}/tasks/{task_id}` - Update a task
- `DELETE /api/{user_id}/tasks/{task_id}` - Delete a task

**Note**: All task endpoints require a valid JWT token in the Authorization header and the user_id in the path must match the authenticated user.

## Environment Variables

### Backend (.env)
- `NEON_DB_URL`: PostgreSQL connection string from Neon DB
- `BETTER_AUTH_SECRET`: Secret key for JWT token signing (use a strong random string)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: JWT token expiration time (default: 30)
- `DEBUG`: Enable debug mode (true/false)

### Frontend (.env.local)
- `NEXT_PUBLIC_API_URL`: Backend API base URL (default: http://127.0.0.1:8080)

## Running Tests
- Backend: `pytest tests/` (tests not yet implemented)
- Frontend: `npm run test` (tests not yet implemented)

## Features
- ✅ User authentication with JWT tokens
- ✅ User-specific task isolation
- ✅ Create, read, update, delete tasks
- ✅ Task status management (pending/completed)
- ✅ Dark/light mode theme support
- ✅ Responsive design for mobile and desktop
- ✅ Smooth animations with Framer Motion
- ✅ Real-time error handling and validation

## Troubleshooting

### Backend won't start
- Verify your `NEON_DB_URL` is correct
- Check that port 8080 is not already in use
- Ensure all Python dependencies are installed

### Frontend can't connect to backend
- Verify the backend is running on port 8080
- Check that `NEXT_PUBLIC_API_URL` in `.env.local` matches the backend URL
- Check browser console for CORS errors

### Login fails with 422 error
- Ensure you're using the correct email and password
- Check that the backend is running and database is accessible
- Verify the user exists in the database

### Can't see tasks after login
- Verify you're logged in (check for JWT token in browser localStorage)
- Check browser console for API errors
- Ensure the backend is running and accessible
