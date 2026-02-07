# API Contract: Todo Application

## Base URL
`http://localhost:8000/api/v1` (development)
`https://[domain]/api/v1` (production)

## Authentication
None required for basic Todo application (would be added for multi-user support)

## Endpoints

### GET /tasks
**Description**: Retrieve all tasks
**Method**: GET
**Path**: `/tasks`
**Query Parameters**:
- `status` (optional): Filter by status ('pending', 'completed')
- `limit` (optional): Limit number of results
- `offset` (optional): Offset for pagination

**Response**:
- Status Code: 200 OK
- Body:
```json
{
  "tasks": [
    {
      "id": "uuid-string",
      "title": "string",
      "description": "string or null",
      "status": "pending|completed",
      "created_at": "ISO 8601 datetime string",
      "updated_at": "ISO 8601 datetime string"
    }
  ],
  "total": integer
}
```

**Error Responses**:
- 500: Internal Server Error

### POST /tasks
**Description**: Create a new task
**Method**: POST
**Path**: `/tasks`

**Request Body**:
```json
{
  "title": "string (required)",
  "description": "string (optional, can be null)"
}
```

**Response**:
- Status Code: 201 Created
- Body:
```json
{
  "id": "uuid-string",
  "title": "string",
  "description": "string or null",
  "status": "pending",
  "created_at": "ISO 8601 datetime string",
  "updated_at": "ISO 8601 datetime string"
}
```

**Error Responses**:
- 400: Bad Request (validation error - e.g., empty title)
- 422: Unprocessable Entity (validation error)
- 500: Internal Server Error

### PATCH /tasks/{task_id}
**Description**: Update an existing task (status or details)
**Method**: PATCH
**Path**: `/tasks/{task_id}`

**Path Parameters**:
- `task_id`: UUID string identifier of the task

**Request Body** (partial updates allowed):
```json
{
  "title": "string (optional)",
  "description": "string (optional)",
  "status": "pending|completed (optional)"
}
```

**Response**:
- Status Code: 200 OK
- Body:
```json
{
  "id": "uuid-string",
  "title": "string",
  "description": "string or null",
  "status": "pending|completed",
  "created_at": "ISO 8601 datetime string",
  "updated_at": "ISO 8601 datetime string"
}
```

**Error Responses**:
- 400: Bad Request (validation error)
- 404: Not Found (task does not exist)
- 422: Unprocessable Entity (validation error)
- 500: Internal Server Error

### DELETE /tasks/{task_id}
**Description**: Delete a task
**Method**: DELETE
**Path**: `/tasks/{task_id}`

**Path Parameters**:
- `task_id`: UUID string identifier of the task

**Response**:
- Status Code: 204 No Content

**Error Responses**:
- 404: Not Found (task does not exist)
- 500: Internal Server Error

## Common Error Response Format
```json
{
  "detail": "Human-readable error message"
}
```

## Validation Rules
- Title must not be empty or consist only of whitespace
- Status must be one of: 'pending', 'completed'
- Description, if provided, must not exceed 1000 characters