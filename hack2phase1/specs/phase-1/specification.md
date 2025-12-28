# Feature Specification: Phase 1 - In-Memory Todo Console Application

**Feature Branch**: `phase-1-todo-app`
**Created**: 2025-12-28
**Status**: Complete
**Version**: 1.0

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Add a New Task (Priority: P1)

As a user, I need to be able to add a new task to my todo list with a title, so that I can track things I need to do.

**Why this priority**: This is the foundation feature. Without the ability to create tasks, the todo app has no purpose. Every other feature depends on tasks existing.

**Independent Test**: Can be fully tested by launching the app, selecting "Add Task", entering a task title, and verifying the task appears in the task list with a unique ID and "PENDING" status.

**Acceptance Scenarios**:

1. **Given** the app is running and showing the main menu, **When** user selects "Add Task" and enters a valid task title (1-200 characters), **Then** the system creates a new task with a unique ID, PENDING status, and current timestamp, and displays a success message with the task ID.

2. **Given** the user is adding a task, **When** they enter an empty title or a title longer than 200 characters, **Then** the system displays an error message and prompts for valid input without creating a task.

3. **Given** multiple tasks have been added, **When** a new task is added, **Then** the new task receives the next sequential ID (monotonically increasing).

---

### User Story 2 - View All Tasks (Priority: P1)

As a user, I need to see all tasks in my list, so that I can understand what I need to do.

**Why this priority**: Critical for usability. Users need visibility into their task list to make decisions about what to work on next.

**Independent Test**: Can be tested by adding several tasks, selecting "View All Tasks", and verifying all tasks are displayed with their IDs, titles, and status.

**Acceptance Scenarios**:

1. **Given** the app has multiple tasks, **When** the user selects "View All Tasks", **Then** all tasks are displayed in a readable format showing ID, title, status, and creation timestamp.

2. **Given** the app has no tasks, **When** the user selects "View All Tasks", **Then** the system displays a message indicating the task list is empty.

3. **Given** tasks are displayed, **When** a task is marked as COMPLETED, **Then** the display shows both creation and completion timestamps for that task.

---

### User Story 3 - Mark Task as Complete (Priority: P1)

As a user, I need to mark tasks as complete when I finish them, so that I can track progress and distinguish done from undone work.

**Why this priority**: Core feature for task management. Users need the ability to mark progress to have any sense of accomplishment.

**Independent Test**: Can be tested by adding a task, selecting "Mark Task Complete", entering the task ID, and verifying the task status changes to COMPLETED with a completion timestamp.

**Acceptance Scenarios**:

1. **Given** a task with PENDING status exists, **When** the user selects "Mark Task Complete" and enters the task's ID, **Then** the task status changes to COMPLETED, a completion timestamp is recorded, and a success message is displayed.

2. **Given** the user is marking a task complete, **When** they enter an invalid ID (task doesn't exist), **Then** the system displays an error message and does not modify any tasks.

3. **Given** a task is already COMPLETED, **When** the user attempts to mark it complete again, **Then** the system either prevents the action or handles it gracefully (resets timestamp or shows message).

---

### User Story 4 - Delete a Task (Priority: P1)

As a user, I need to delete tasks, so that I can remove items that are no longer relevant or were added by mistake.

**Why this priority**: Essential for task list maintenance. Users need the ability to clean up their task list.

**Independent Test**: Can be tested by adding a task, selecting "Delete Task", entering the task ID, and verifying the task is removed from the list.

**Acceptance Scenarios**:

1. **Given** a task exists in the task list, **When** the user selects "Delete Task" and enters the task's ID, **Then** the task is removed from the list and a success message is displayed.

2. **Given** the user is deleting a task, **When** they enter an invalid ID, **Then** the system displays an error message and no tasks are deleted.

3. **Given** a task has been deleted, **When** the user views the task list, **Then** the deleted task does not appear.

---

### User Story 5 - Filter Tasks by Status (Priority: P2)

As a user, I need to see only pending or completed tasks, so that I can focus on what still needs to be done or review what I've accomplished.

**Why this priority**: Enhances usability for users with large task lists. Allows users to filter their view to show only relevant tasks. Important but not as critical as basic CRUD operations.

**Independent Test**: Can be tested by adding multiple tasks with mixed statuses, selecting "View Pending" or "View Completed", and verifying only tasks with the selected status are displayed.

**Acceptance Scenarios**:

1. **Given** the app has both pending and completed tasks, **When** the user selects "View Pending Tasks", **Then** only tasks with PENDING status are displayed.

2. **Given** the app has both pending and completed tasks, **When** the user selects "View Completed Tasks", **Then** only tasks with COMPLETED status are displayed.

3. **Given** the user is viewing filtered tasks and no tasks match the filter, **Then** the system displays a message indicating no tasks match the current filter.

---

### Edge Cases

- What happens when a user attempts to add a task with whitespace-only title (e.g., "   ")? → Should be treated as empty and rejected.
- What happens when a user tries to mark a non-existent task as complete or delete it? → System should display a clear error and not crash.
- What happens if the user enters invalid menu choices (e.g., "7", "abc", "-1")? → System should reprompt for valid input.
- What happens if a task title contains special characters or very long strings? → Should be accepted as long as it's 1-200 characters.
- What happens when the app is exited? → All data is lost (in-memory only; Phase 2 will add persistence).

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to add a new task with a title (1-200 characters)
- **FR-002**: System MUST assign a unique, monotonically increasing integer ID to each task
- **FR-003**: System MUST record the creation timestamp for each task in ISO 8601 format (UTC)
- **FR-004**: System MUST allow users to view all tasks with their ID, title, status, and timestamps
- **FR-005**: System MUST allow users to mark a task as COMPLETED and record the completion timestamp
- **FR-006**: System MUST allow users to delete a task by its ID
- **FR-007**: System MUST allow users to filter tasks by status (PENDING or COMPLETED)
- **FR-008**: System MUST validate task titles on input (non-empty, ≤200 characters)
- **FR-009**: System MUST validate user input for task IDs before operations (must exist and be a valid integer)
- **FR-010**: System MUST display clear, user-friendly error messages when operations fail
- **FR-011**: System MUST maintain a consistent menu system that users can navigate
- **FR-012**: System MUST prevent application crashes on user input errors; always return to main menu after operations

### Key Entities

- **Task**: Represents a single todo item with the following attributes:
  - `id` (integer): Unique identifier, auto-assigned, monotonically increasing
  - `title` (string): Description of the task, 1-200 characters, trimmed whitespace
  - `status` (enum): Either PENDING or COMPLETED
  - `created_at` (timestamp): ISO 8601 format, UTC, set at creation
  - `completed_at` (timestamp, optional): ISO 8601 format, UTC, only set when marked complete

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can add a new task and see it in the task list within 1 second of confirmation
- **SC-002**: System displays all tasks in under 50 milliseconds (p95) for lists up to 1000 tasks
- **SC-003**: Users can navigate the menu and complete operations (add, view, mark complete, delete) without the application crashing
- **SC-004**: All 5 core features (Add, View, Update/Mark Complete, Delete, Filter) are fully functional and testable
- **SC-005**: 100% of user input is validated; invalid input results in clear error messages, not application errors
- **SC-006**: Task list is maintained correctly across multiple sequential operations (add → view → mark complete → delete)
- **SC-007**: Unique sequential IDs are correctly assigned to all tasks without reuse or gaps

---

## Constraints & Assumptions

### Constraints

- Phase 1 is in-memory only; no data persistence to disk
- No external CLI frameworks (Click, Typer, Rich); use standard Python input()/print()
- No external dependencies beyond Python standard library (except pytest/mypy/flake8 for development)
- Single-user console application; no multi-threaded access
- Python 3.13+ required

### Assumptions

- Users have basic terminal/console access and can run Python applications
- Users understand numbered menu systems
- Task titles do not need special markdown or formatting; plain text is sufficient
- Timestamps in ISO 8601 UTC format are acceptable for display
- Lexicographic ordering of tasks by ID is sufficient (no custom sorting required)
- Users will exit the application cleanly via the menu option (data loss on exit is acceptable for Phase 1)

---

## Implementation Roadmap *(informational)*

This specification will be implemented following the Spec-Driven Development methodology:

1. **Architecture Plan** (`specs/phase-1/plan.md`): Defines layered architecture (UI → Operations → Storage → Models)
2. **Task Breakdown** (`specs/phase-1/tasks.md`): Decomposes plan into 23 granular, testable TDD tasks
3. **Test-First Development**: Each task includes acceptance criteria in Given-When-Then format
4. **Code Quality Gates**: Type checking (mypy --strict), linting (flake8), ≥90% test coverage

---

**Specification Complete.** Ready for architecture planning and task breakdown.
