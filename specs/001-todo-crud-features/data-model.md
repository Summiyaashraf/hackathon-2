# Data Model: Todo Application

## Task Entity

### Fields
- **id** (UUID/Integer): Primary key, unique identifier for the task
- **title** (String, required): The title of the task, cannot be empty
- **description** (String, optional): Optional detailed description of the task
- **status** (String/Enum): Current status of the task ('pending' or 'completed'), defaults to 'pending'
- **created_at** (DateTime): Timestamp when the task was created, auto-generated
- **updated_at** (DateTime): Timestamp when the task was last updated, auto-generated

### Validation Rules
- Title must not be empty or consist only of whitespace
- Status must be one of the allowed values: 'pending', 'completed'
- Description, if provided, must not exceed 1000 characters

### State Transitions
- From 'pending' to 'completed': When user marks task as done
- From 'completed' to 'pending': When user unmarks task as done

### Relationships
- No relationships required for basic Todo application