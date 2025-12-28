# Phase 1 Implementation Task Breakdown

**Status**: Ready for Implementation
**Created**: 2025-12-28
**Total Tasks**: 23
**Estimated Duration**: 34.5 hours
**Dependencies**: Specification ✅, Architecture Plan ✅

---

## Task Organization

Tasks are organized in dependency order across 7 categories. Each task includes:
- **Complexity**: Simple (~1-2 hours) | Medium (~2-4 hours) | Complex (~4+ hours)
- **Dependencies**: Tasks that must complete first
- **Acceptance Criteria**: Given-When-Then format from specification
- **TDD Workflow**: Red → Green → Refactor guidance

---

## Category 1: Project Setup (5 tasks)

### T-001: Configure UV Project & Dependencies

**Complexity**: Simple (1 hour)
**Dependencies**: None

**Description**: Set up the Python project configuration with UV, establishing the foundation for all development.

**Files to Create/Modify**:
- `pyproject.toml` (new)
- `.venv/` (created by UV)

**Acceptance Criteria**:

- **Given** the project directory exists, **When** running `uv sync`, **Then** a virtual environment is created and all dependencies are installed
- **Given** the project is set up, **When** running `python --version` in the venv, **Then** Python 3.13+ is active
- **Given** development dependencies are configured, **When** running `uv run pytest --version`, **Then** pytest is available
- **Given** the project is set up, **When** running `uv run mypy --version`, **Then** mypy is available in strict mode

**TDD Workflow**:
1. **Red**: Verify pyproject.toml does not exist yet
2. **Green**: Create minimal pyproject.toml with required dependencies:
   - Runtime: none (stdlib only)
   - Dev: pytest, pytest-cov, mypy, flake8, black
3. **Refactor**: Document dependency rationale in comments

**Spec Reference**: CLAUDE.md "Dependency Management via UV" section

---

### T-002: Create Source Directory Structure

**Complexity**: Simple (0.5 hours)
**Dependencies**: T-001

**Description**: Create the package directory structure for the todo application.

**Files to Create**:
- `src/todo/__init__.py`
- `src/todo/models/__init__.py`
- `src/todo/storage/__init__.py`
- `src/todo/operations/__init__.py`
- `src/todo/ui/__init__.py`

**Acceptance Criteria**:

- **Given** the source structure is created, **When** running `ls -R src/`, **Then** all required subdirectories exist with __init__.py files
- **Given** the package is set up, **When** running `python -c "import todo; print('OK')"`, **Then** the module imports without errors

**TDD Workflow**:
1. **Red**: Verify directories don't exist
2. **Green**: Create all directories and __init__.py files
3. **Refactor**: N/A (structural task)

**Spec Reference**: Plan section 2 "Directory Structure"

---

### T-003: Create Test Directory Structure

**Complexity**: Simple (0.5 hours)
**Dependencies**: T-001

**Description**: Create the test directory structure with unit and integration test folders.

**Files to Create**:
- `tests/__init__.py`
- `tests/unit/__init__.py`
- `tests/unit/conftest.py` (pytest fixtures)
- `tests/integration/__init__.py`
- `tests/integration/conftest.py` (pytest fixtures)

**Acceptance Criteria**:

- **Given** test structure is created, **When** running `uv run pytest --collect-only`, **Then** pytest discovers the test directories
- **Given** conftest.py files exist, **When** running `uv run pytest`, **Then** no import errors occur

**TDD Workflow**:
1. **Red**: Verify test directories don't exist
2. **Green**: Create directories and empty conftest.py files
3. **Refactor**: N/A (structural task)

**Spec Reference**: Plan section 6 "Testing Strategy"

---

### T-004: Create Main Entry Point (main.py)

**Complexity**: Medium (2 hours)
**Dependencies**: T-002

**Description**: Create the main.py file with basic application loop structure (not yet functional).

**Files to Create**:
- `src/todo/main.py`

**Acceptance Criteria**:

- **Given** main.py exists, **When** running `uv run python -m todo.main`, **Then** the application starts and displays a welcome message
- **Given** the app is running, **When** user enters "0" (exit), **Then** the application terminates gracefully with an exit message
- **Given** main.py is imported, **When** type checking runs `uv run mypy src/todo/main.py --strict`, **Then** no type errors occur

**TDD Workflow**:
1. **Red**: Write a test that calls main() and expects no exceptions
2. **Green**: Implement minimal main() with basic loop and exit handling
3. **Refactor**: Ensure type hints are complete

**Spec Reference**: Plan section 5 "UI/UX Flow", CLAUDE.md "Run the Application" section

---

### T-005: Verify Quality Gate Configuration

**Complexity**: Simple (1 hour)
**Dependencies**: T-001, T-002, T-003, T-004

**Description**: Verify that all quality tools can run successfully without errors.

**Acceptance Criteria**:

- **Given** the project is set up, **When** running `uv run mypy src/todo --strict`, **Then** no errors occur (all files pass type checking)
- **Given** the project is set up, **When** running `uv run flake8 src/todo --max-line-length=100`, **Then** no linting errors occur
- **Given** the project is set up, **When** running `uv run pytest tests/ -v`, **Then** pytest runs without collection errors (even if no tests yet)

**TDD Workflow**:
1. **Red**: Run all quality tools; expect failures until code is type-hinted
2. **Green**: Add type hints to all code files until tools pass
3. **Refactor**: Ensure no issues remain

**Spec Reference**: CLAUDE.md "Quality Checks" section

---

## Category 2: Data Models (3 tasks)

### T-006: Implement Task Dataclass

**Complexity**: Medium (2 hours)
**Dependencies**: T-002

**Description**: Create the Task dataclass with validation, status enum, and immutability semantics.

**Files to Create/Modify**:
- `src/todo/models/task.py` (new)
- `src/todo/models/__init__.py` (export Task, TaskStatus)

**Acceptance Criteria**:

- **Given** the Task class is created, **When** instantiating Task with valid parameters, **Then** a Task object is created with id, title, status, created_at, and optional completed_at
- **Given** a Task has status=COMPLETED, **When** accessing the Task, **Then** completed_at contains an ISO 8601 timestamp
- **Given** a Task with title="" is created, **When** __post_init__ runs, **Then** ValueError is raised with message containing "1-200 chars"
- **Given** a Task with title longer than 200 chars is created, **When** __post_init__ runs, **Then** ValueError is raised
- **Given** a COMPLETED task with no completed_at, **When** __post_init__ runs, **Then** ValueError is raised
- **Given** a TaskStatus enum exists, **When** accessing TaskStatus.PENDING and TaskStatus.COMPLETED, **Then** both values are available as strings

**TDD Workflow**:
1. **Red**: Write unit tests for Task creation, validation, and status transitions; all fail
2. **Green**: Implement Task dataclass with __post_init__ validation
3. **Refactor**: Ensure slots=True is used for memory efficiency; optimize __post_init__ logic

**Spec Reference**: Specification "Key Entities", Plan section 3 "Data Model Design"

---

### T-007: Write Unit Tests for Task Model

**Complexity**: Medium (2 hours)
**Dependencies**: T-003, T-006

**Description**: Create comprehensive unit tests for the Task dataclass covering all validation rules and edge cases.

**Files to Create**:
- `tests/unit/test_task.py` (new)

**Acceptance Criteria**:

- **Given** test_task.py is created, **When** running `uv run pytest tests/unit/test_task.py -v`, **Then** at least 8 tests pass covering:
  - Valid task creation
  - Title validation (empty, too long, valid)
  - Status enum values
  - Timestamp generation and validation
  - COMPLETED task validation (requires completed_at)
  - Task equality and representation

**TDD Workflow**:
1. **Red**: Write comprehensive test suite for Task class
2. **Green**: Ensure all Task class tests pass
3. **Refactor**: Consolidate test helper functions if needed

**Spec Reference**: Specification "Functional Requirements FR-001 to FR-003", "Edge Cases"

---

### T-008: Export Task Model from todo Package

**Complexity**: Simple (0.5 hours)
**Dependencies**: T-006

**Description**: Update package exports so Task and TaskStatus are available from `todo.models`.

**Files to Modify**:
- `src/todo/models/__init__.py` (add exports)
- `src/todo/__init__.py` (optional, for convenience imports)

**Acceptance Criteria**:

- **Given** the models package is set up, **When** running `python -c "from todo.models import Task, TaskStatus; print('OK')"`, **Then** imports succeed
- **Given** main.py or other modules use Task, **When** running `uv run mypy src/todo --strict`, **Then** type checking passes

**TDD Workflow**:
1. **Red**: Try importing Task from wrong location; expect ImportError
2. **Green**: Add exports to __init__.py
3. **Refactor**: Verify no circular imports

**Spec Reference**: Plan section 4 "Module Responsibility Matrix"

---

## Category 3: Storage Layer (3 tasks)

### T-009: Implement InMemoryStorage Class

**Complexity**: Medium (2.5 hours)
**Dependencies**: T-008

**Description**: Create the in-memory storage backend using Dict[int, Task] with CRUD operations.

**Files to Create**:
- `src/todo/storage/in_memory.py` (new)

**Acceptance Criteria**:

- **Given** InMemoryStorage is instantiated, **When** calling add("Buy milk"), **Then** a Task is created with auto-assigned ID and returned
- **Given** a task has been added, **When** calling get(task_id), **Then** the Task is returned; calling get(invalid_id) returns None
- **Given** a task exists, **When** calling update(task_id, status=COMPLETED), **Then** the task status changes and completed_at is set
- **Given** a task exists, **When** calling delete(task_id), **Then** the task is removed and True is returned; delete(invalid_id) returns False
- **Given** multiple tasks are added, **When** calling list_all(), **Then** a list of all Task objects is returned in order
- **Given** multiple tasks are added, **When** checking IDs, **Then** IDs are monotonically increasing with no gaps

**TDD Workflow**:
1. **Red**: Write storage tests for all CRUD operations; all fail
2. **Green**: Implement InMemoryStorage with Dict[int, Task] and auto-increment counter
3. **Refactor**: Optimize ID generation; add docstrings

**Spec Reference**: Plan section 3 "Storage Mechanism", Specification "FR-002, FR-003"

---

### T-010: Write Unit Tests for Storage

**Complexity**: Medium (2 hours)
**Dependencies**: T-003, T-009

**Description**: Create comprehensive unit tests for InMemoryStorage covering all CRUD operations.

**Files to Create**:
- `tests/unit/test_storage.py` (new)

**Acceptance Criteria**:

- **Given** test_storage.py is created, **When** running `uv run pytest tests/unit/test_storage.py -v`, **Then** at least 10 tests pass covering:
  - add() with valid title
  - get() for existing and non-existent IDs
  - update() for status and timestamp changes
  - delete() for existing and non-existent IDs
  - list_all() empty and populated
  - ID generation monotonicity

**TDD Workflow**:
1. **Red**: Write comprehensive test suite for storage
2. **Green**: Ensure all tests pass
3. **Refactor**: Consolidate repeated setup logic in fixtures

**Spec Reference**: Plan section 6 "Unit Test Structure"

---

### T-011: Export Storage from Package

**Complexity**: Simple (0.5 hours)
**Dependencies**: T-009

**Description**: Update package exports for InMemoryStorage.

**Files to Modify**:
- `src/todo/storage/__init__.py` (add exports)

**Acceptance Criteria**:

- **Given** the storage package is set up, **When** running `python -c "from todo.storage import InMemoryStorage; print('OK')"`, **Then** import succeeds

**TDD Workflow**:
1. **Red**: Try importing InMemoryStorage from wrong location
2. **Green**: Add exports to __init__.py
3. **Refactor**: Verify no circular imports

**Spec Reference**: Plan section 4 "Module Responsibility Matrix"

---

## Category 4: Operations Layer (4 tasks)

### T-012: Implement TaskOperations Class

**Complexity**: Complex (4 hours)
**Dependencies**: T-011

**Description**: Create the business logic layer that orchestrates operations using storage and models.

**Files to Create**:
- `src/todo/operations/task_operations.py` (new)

**Acceptance Criteria**:

- **Given** TaskOperations is instantiated with a storage backend, **When** calling add_task("Buy milk"), **Then** a Task is created via storage with validation
- **Given** TaskOperations exists, **When** calling mark_complete(task_id) with valid ID, **Then** storage is updated with COMPLETED status and timestamp
- **Given** TaskOperations exists, **When** calling mark_complete(invalid_id), **Then** NotFoundError is raised
- **Given** TaskOperations exists, **When** calling delete_task(task_id), **Then** storage.delete() is called and result is returned
- **Given** TaskOperations exists, **When** calling list_tasks(), **Then** all tasks are returned from storage
- **Given** TaskOperations exists, **When** calling filter_by_status(PENDING), **Then** only PENDING tasks are returned
- **Given** TaskOperations exists, **When** calling filter_by_status(COMPLETED), **Then** only COMPLETED tasks are returned

**TDD Workflow**:
1. **Red**: Write tests for all operations methods; all fail
2. **Green**: Implement TaskOperations class with business logic
3. **Refactor**: Extract validation logic; add error handling

**Spec Reference**: Plan section 4 "Public APIs", Specification "FR-001 to FR-007"

---

### T-013: Write Unit Tests for Operations

**Complexity**: Medium (2.5 hours)
**Dependencies**: T-003, T-012

**Description**: Create comprehensive unit tests for TaskOperations covering all business logic.

**Files to Create**:
- `tests/unit/test_operations.py` (new)

**Acceptance Criteria**:

- **Given** test_operations.py is created, **When** running `uv run pytest tests/unit/test_operations.py -v`, **Then** at least 15 tests pass covering:
  - add_task() with valid and invalid titles
  - mark_complete() with valid and invalid IDs
  - delete_task() with valid and invalid IDs
  - list_tasks() empty and populated
  - filter_by_status() for PENDING and COMPLETED
  - All error cases raise appropriate exceptions

**TDD Workflow**:
1. **Red**: Write comprehensive test suite for operations
2. **Green**: Ensure all tests pass
3. **Refactor**: Use fixtures for storage setup

**Spec Reference**: Plan section 6 "Unit Test Structure"

---

### T-014: Implement Exception Hierarchy

**Complexity**: Simple (1 hour)
**Dependencies**: T-002

**Description**: Create custom exceptions for the application.

**Files to Create**:
- `src/todo/operations/exceptions.py` (new) OR add to task_operations.py

**Acceptance Criteria**:

- **Given** exceptions are defined, **When** importing TodoAppError, ValidationError, NotFoundError, **Then** all are available
- **Given** exceptions are raised, **When** catching ValidationError, **Then** the exception contains a descriptive message
- **Given** exceptions are caught in main, **When** a NotFoundError is raised, **Then** main displays an appropriate error message

**TDD Workflow**:
1. **Red**: Try catching exceptions that don't exist yet
2. **Green**: Define exception classes with docstrings
3. **Refactor**: Ensure all code uses custom exceptions consistently

**Spec Reference**: Plan section 7 "Exception Hierarchy"

---

### T-015: Export Operations from Package

**Complexity**: Simple (0.5 hours)
**Dependencies**: T-012, T-014

**Description**: Update package exports for TaskOperations and exceptions.

**Files to Modify**:
- `src/todo/operations/__init__.py` (add exports)

**Acceptance Criteria**:

- **Given** the operations package is set up, **When** running `python -c "from todo.operations import TaskOperations, ValidationError; print('OK')"`, **Then** imports succeed

**TDD Workflow**:
1. **Red**: Try importing from wrong locations
2. **Green**: Add exports to __init__.py
3. **Refactor**: Verify no circular imports

**Spec Reference**: Plan section 4 "Module Responsibility Matrix"

---

## Category 5: UI Layer (3 tasks)

### T-016: Implement Display Formatting

**Complexity**: Medium (1.5 hours)
**Dependencies**: T-008

**Description**: Create display formatting functions for tasks.

**Files to Create**:
- `src/todo/ui/display.py` (new)

**Acceptance Criteria**:

- **Given** a Task object exists, **When** calling format_task(task), **Then** a formatted string is returned with ID, title, status, and timestamps
- **Given** multiple tasks exist, **When** calling print_tasks(tasks, title="My Tasks"), **Then** all tasks are displayed with the provided title
- **Given** the task list is empty, **When** calling print_tasks([], title="Tasks"), **Then** a message indicating the list is empty is displayed
- **Given** a task is COMPLETED, **When** formatting it, **Then** both created_at and completed_at timestamps are shown

**TDD Workflow**:
1. **Red**: Write tests for format_task() and print_tasks()
2. **Green**: Implement formatting functions with string templates
3. **Refactor**: Ensure output is readable and matches spec examples

**Spec Reference**: Plan section 5 "Task Display Format", Specification "FR-004"

---

### T-017: Implement Menu System

**Complexity**: Medium (2 hours)
**Dependencies**: T-002

**Description**: Create the menu display and input handling logic.

**Files to Create**:
- `src/todo/ui/menu.py` (new)

**Acceptance Criteria**:

- **Given** the menu is displayed, **When** the user is presented with 6 options (1-6) plus exit (0), **Then** each option is clearly labeled
- **Given** the user enters a valid choice (0-6), **When** get_user_choice() is called, **Then** the choice is returned as an integer
- **Given** the user enters an invalid choice (e.g., "abc", "7"), **When** get_user_choice() is called, **Then** an error is displayed and the user is re-prompted
- **Given** the user enters menu choice "1" (Add Task), **When** a helper function returns the choice, **Then** main.py can determine which operation to perform

**TDD Workflow**:
1. **Red**: Write tests for menu display and input validation
2. **Green**: Implement menu functions with input validation
3. **Refactor**: Extract menu strings to constants

**Spec Reference**: Plan section 5 "Menu System Design", Specification "FR-011"

---

### T-018: Export UI Functions from Package

**Complexity**: Simple (0.5 hours)
**Dependencies**: T-016, T-017

**Description**: Update package exports for UI functions.

**Files to Modify**:
- `src/todo/ui/__init__.py` (add exports)

**Acceptance Criteria**:

- **Given** the UI package is set up, **When** running `python -c "from todo.ui import format_task, print_tasks, display_menu; print('OK')"`, **Then** imports succeed

**TDD Workflow**:
1. **Red**: Try importing from wrong locations
2. **Green**: Add exports to __init__.py
3. **Refactor**: Verify no circular imports

**Spec Reference**: Plan section 4 "Module Responsibility Matrix"

---

## Category 6: Main Application (2 tasks)

### T-019: Implement Full Application Loop (main.py)

**Complexity**: Complex (3 hours)
**Dependencies**: T-015, T-018

**Description**: Integrate all layers into a complete, functional application loop.

**Files to Modify**:
- `src/todo/main.py` (expand from T-004)

**Acceptance Criteria**:

- **Given** the app is running, **When** user selects "1" (Add Task) and enters a valid title, **Then** the task is created and success message is displayed
- **Given** the app is running, **When** user selects "2" (View All), **Then** all tasks are displayed or a message if none exist
- **Given** the app is running, **When** user selects "3" (View Pending), **Then** only PENDING tasks are displayed
- **Given** the app is running, **When** user selects "4" (View Completed), **Then** only COMPLETED tasks are displayed
- **Given** the app is running, **When** user selects "5" (Mark Complete) with valid ID, **Then** task status changes and success message is displayed
- **Given** the app is running, **When** user selects "6" (Delete) with valid ID, **Then** task is deleted and success message is displayed
- **Given** the app is running, **When** user enters invalid task ID, **Then** error message is displayed and menu returns
- **Given** the app is running, **When** user selects "0" (Exit), **Then** application terminates gracefully
- **Given** any error occurs during an operation, **When** the error is caught, **Then** error is displayed and menu returns (no crash)

**TDD Workflow**:
1. **Red**: Write integration test for full app flow
2. **Green**: Implement complete main() loop with all menu options
3. **Refactor**: Extract operation handlers into helper functions if main() becomes too long

**Spec Reference**: Specification "User Stories 1-5", Plan section 5 "UI/UX Flow"

---

### T-020: Create README.md

**Complexity**: Simple (1 hour)
**Dependencies**: T-019

**Description**: Write user-facing documentation for the application.

**Files to Create**:
- `README.md` (new)

**Acceptance Criteria**:

- **Given** README.md exists, **When** reading it, **Then** it explains how to run the application and what features are available
- **Given** a new user follows the README, **When** they run the app, **Then** they can successfully use all features

**TDD Workflow**:
1. **Red**: No README exists
2. **Green**: Create README with installation, usage, and feature overview
3. **Refactor**: Ensure clarity and completeness

**Spec Reference**: CLAUDE.md "Run the Application" section

---

## Category 7: Quality Assurance (3 tasks)

### T-021: Write Integration Tests

**Complexity**: Complex (3 hours)
**Dependencies**: T-019

**Description**: Create integration tests covering full workflows.

**Files to Create**:
- `tests/integration/test_workflows.py` (new)
- `tests/integration/test_full_application.py` (new)

**Acceptance Criteria**:

- **Given** integration tests are written, **When** running `uv run pytest tests/integration/ -v`, **Then** at least 6 tests pass covering:
  - Full task lifecycle (add → view → mark complete → delete)
  - Multiple operations independence
  - ID generation monotonicity
  - Status filter correctness
  - Error handling across layers
  - Concurrent operations (sequential operations preserving state)

**TDD Workflow**:
1. **Red**: Write end-to-end tests without mocking storage
2. **Green**: Ensure all integration tests pass
3. **Refactor**: Consolidate setup logic in conftest.py

**Spec Reference**: Plan section 6 "Integration Test Scenarios"

---

### T-022: Verify Test Coverage & Quality Gates

**Complexity**: Medium (1.5 hours)
**Dependencies**: T-007, T-010, T-013, T-021

**Description**: Run all quality checks and verify coverage meets targets.

**Acceptance Criteria**:

- **Given** all tests are written, **When** running `uv run pytest tests/ --cov=src/todo --cov-report=term-missing`, **Then** coverage is ≥90%
- **Given** critical paths are tested, **When** running coverage report, **Then** add(), mark_complete(), delete() have 100% coverage
- **Given** all code is written, **When** running `uv run mypy src/todo --strict`, **Then** no type errors occur
- **Given** all code is written, **When** running `uv run flake8 src/todo --max-line-length=100`, **Then** no linting errors occur
- **Given** all tests pass, **When** running `uv run pytest tests/ -v`, **Then** all tests pass with 0 failures

**TDD Workflow**:
1. **Red**: Run all quality tools; capture failures
2. **Green**: Fix type errors, linting issues, and increase coverage
3. **Refactor**: Ensure no hardcoded secrets; validate error handling

**Spec Reference**: CLAUDE.md "Code Quality Checks", Plan section 11 "Quality Gates"

---

### T-023: Final Documentation & Completion

**Complexity**: Simple (1 hour)
**Dependencies**: T-022

**Description**: Complete documentation and verify Phase 1 completion checklist.

**Files to Modify**:
- `CLAUDE.md` (update Implementation status)
- `specs/phase-1/tasks.md` (mark all complete)

**Acceptance Criteria**:

- **Given** all tasks are complete, **When** reviewing the checklist in CLAUDE.md, **Then** all Phase 1 items are marked ✅
- **Given** the app is ready, **When** following CLAUDE.md instructions, **Then** the app can be run and all features work
- **Given** the code is complete, **When** a fresh user clones the repo and runs `uv sync && uv run python -m todo.main`, **Then** the app starts and works

**TDD Workflow**:
1. **Red**: Checklist shows incomplete items
2. **Green**: Complete all items and mark checklist
3. **Refactor**: Ensure documentation is accurate

**Spec Reference**: CLAUDE.md "Constitutional Compliance Checklist"

---

## Summary

| Category | Tasks | Complexity | Duration |
|----------|-------|-----------|----------|
| Project Setup | 5 | Mixed | 5.5 hours |
| Data Models | 3 | Medium | 4.5 hours |
| Storage Layer | 3 | Medium | 5 hours |
| Operations Layer | 4 | Medium-Complex | 7.5 hours |
| UI Layer | 3 | Medium | 3.5 hours |
| Main Application | 2 | Complex | 4 hours |
| Quality Assurance | 3 | Medium-Complex | 4.5 hours |
| **TOTAL** | **23** | **Varied** | **34.5 hours** |

---

## Dependency Graph

```
T-001 (UV Config)
  ├─→ T-002 (Source Structure)
  │    ├─→ T-004 (main.py)
  │    └─→ T-006 (Task Model)
  │         └─→ T-008 (Exports)
  │              └─→ T-009 (Storage)
  │                   └─→ T-011 (Storage Exports)
  │                        └─→ T-012 (Operations)
  │                             └─→ T-015 (Ops Exports)
  │                                  └─→ T-019 (Main Loop)
  │                                       └─→ T-021 (Integration Tests)
  │                                            └─→ T-022 (QA)
  │                                                 └─→ T-023 (Done)
  │
  ├─→ T-003 (Test Structure)
  │    ├─→ T-007 (Task Tests)
  │    ├─→ T-010 (Storage Tests)
  │    ├─→ T-013 (Operations Tests)
  │    └─→ T-021 (Integration Tests) [see above]
  │
  ├─→ T-005 (QA Config)
  │    └─→ T-022 (Coverage) [see above]
  │
  └─→ T-014 (Exceptions)
       └─→ T-012 (Operations) [see above]

  T-016 (Display)
  └─→ T-018 (UI Exports)
       └─→ T-019 (Main Loop) [see above]

  T-017 (Menu)
  └─→ T-018 (UI Exports) [see above]
```

---

## Phase 1 Completion Checklist

- [ ] T-001: UV Project configured ✅ Ready to implement
- [ ] T-002: Source structure created ✅ Ready to implement
- [ ] T-003: Test structure created ✅ Ready to implement
- [ ] T-004: Main entry point created ✅ Ready to implement
- [ ] T-005: Quality gates verified ✅ Ready to implement
- [ ] T-006: Task dataclass implemented ✅ Ready to implement
- [ ] T-007: Task model tests written ✅ Ready to implement
- [ ] T-008: Task model exports added ✅ Ready to implement
- [ ] T-009: InMemoryStorage implemented ✅ Ready to implement
- [ ] T-010: Storage tests written ✅ Ready to implement
- [ ] T-011: Storage exports added ✅ Ready to implement
- [ ] T-012: TaskOperations implemented ✅ Ready to implement
- [ ] T-013: Operations tests written ✅ Ready to implement
- [ ] T-014: Exception hierarchy defined ✅ Ready to implement
- [ ] T-015: Operations exports added ✅ Ready to implement
- [ ] T-016: Display formatting implemented ✅ Ready to implement
- [ ] T-017: Menu system implemented ✅ Ready to implement
- [ ] T-018: UI exports added ✅ Ready to implement
- [ ] T-019: Full application loop implemented ✅ Ready to implement
- [ ] T-020: README created ✅ Ready to implement
- [ ] T-021: Integration tests written ✅ Ready to implement
- [ ] T-022: Test coverage & quality gates verified ✅ Ready to implement
- [ ] T-023: Final documentation completed ✅ Ready to implement

**Phase 1 Status**: ✅ **Task Breakdown Complete - Ready for Implementation**

---

**Tasks Ready for Implementation.** All 23 tasks defined with clear acceptance criteria and TDD workflow. Proceed with implementation in dependency order starting with T-001.
