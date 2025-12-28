# Phase 1 Todo App - Architecture Plan

**Status:** ✅ Ready for Implementation
**Date:** 2025-12-28
**Version:** 1.0

---

## Executive Summary

This plan designs a clean, modular in-memory todo console application in Python 3.13. It decouples business logic from UI, enables comprehensive testing (90%+ coverage), and provides a foundation for Phase 2 persistence layer. Key design decisions: Dict[int, Task] for O(1) operations, dataclasses with type hints, strict layering between UI/operations/storage/models.

---

## 1. Architecture Overview

### High-Level Design

```
┌─────────────────────────────────────────────────────────┐
│                     Console UI Layer                     │
│  (main.py + ui/menu.py + ui/display.py)                 │
│  • Menu system                                           │
│  • Input validation & prompts                            │
│  • Output formatting                                     │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│                  Operations Layer                        │
│  (operations/task_operations.py)                         │
│  • Business logic: add, update, delete, list, filter     │
│  • Validation enforcement                                │
│  • Error handling & exceptions                           │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│                   Storage Layer                          │
│  (storage/in_memory.py)                                  │
│  • Dict[int, Task] data structure                        │
│  • ID generation (auto-increment)                        │
│  • CRUD primitives                                       │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│                    Data Model                            │
│  (models/task.py)                                        │
│  • Task dataclass                                        │
│  • Status enum                                           │
│  • Validation rules                                      │
└─────────────────────────────────────────────────────────┘
```

### Data Flow

```
User Input → UI Validation → Operations (Business Logic) → Storage → Data Model
     ↓                            ↓
Display ← Formatting ← Operations Result ← Storage Query ← Model Access
```

---

## 2. Directory Structure

```
hack2phase1/
├── src/
│   └── todo/
│       ├── __init__.py
│       ├── main.py                    # Entry point, main loop
│       ├── models/
│       │   ├── __init__.py
│       │   └── task.py                # Task dataclass, Status enum
│       ├── storage/
│       │   ├── __init__.py
│       │   └── in_memory.py           # InMemoryStorage class
│       ├── operations/
│       │   ├── __init__.py
│       │   └── task_operations.py     # TaskOperations class
│       └── ui/
│           ├── __init__.py
│           ├── menu.py                # Menu display & selection
│           └── display.py             # Task formatting & output
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_task.py
│   │   ├── test_storage.py
│   │   └── test_operations.py
│   └── integration/
│       ├── __init__.py
│       └── test_workflows.py
├── pyproject.toml                     # UV project config
├── README.md
├── specs/
│   └── phase-1/
│       ├── spec.md                    # ✅ COMPLETED
│       └── plan.md                    # ✅ THIS FILE
└── specs-history/
    └── phase-1-todo-spec.md           # ✅ COMPLETED
```

**Import Hierarchy:**
```
main.py
  ↓
ui/* ← operations/task_operations.py ← storage/in_memory.py ← models/task.py
```

**Rationale:** Strict layering prevents circular dependencies; models have zero dependencies, storage depends only on models, operations on storage+models, UI on operations+display logic.

---

## 3. Data Model Design

### Task Dataclass (Python 3.13)

```python
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional

class TaskStatus(str, Enum):
    """Task completion status."""
    PENDING = "pending"
    COMPLETED = "completed"

@dataclass(frozen=False, slots=True)
class Task:
    """
    Immutable-by-convention task representation.

    Attributes:
        id: Unique identifier (auto-assigned by storage)
        title: Task description (1-200 chars)
        status: Current completion state
        created_at: ISO 8601 timestamp (UTC)
        completed_at: Completion timestamp (ISO 8601, UTC)
    """
    id: int
    title: str
    status: TaskStatus = TaskStatus.PENDING
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    completed_at: Optional[str] = None

    def __post_init__(self) -> None:
        """Validate task invariants."""
        if not (1 <= len(self.title) <= 200):
            raise ValueError(f"Title must be 1-200 chars, got {len(self.title)}")
        if self.status == TaskStatus.COMPLETED and not self.completed_at:
            raise ValueError("Completed tasks must have completed_at timestamp")
```

**Key Design Choices:**
- `slots=True`: 30% memory reduction for large task lists
- `frozen=False`: Allow status updates (mutability needed for mark_complete)
- String-based enum: Direct JSON serialization for Phase 2
- ISO 8601 timestamps: Standard format, timezone-aware, sortable
- `__post_init__`: Early validation catches invariant violations

### Storage Mechanism

```python
class InMemoryStorage:
    """
    Thread-unsafe in-memory task storage.

    Attributes:
        _tasks: Dict[int, Task] - O(1) lookup by ID
        _next_id: int - Monotonic counter for ID generation
    """
    def __init__(self) -> None:
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1

    def _generate_id(self) -> int:
        """Generate unique task ID (auto-increment)."""
        current_id = self._next_id
        self._next_id += 1
        return current_id
```

**Rationale:**
- **Dict over List:** O(1) lookup/update/delete vs O(n); critical for filtering operations
- **Auto-increment IDs:** Simpler than UUIDs, sufficient for single-user Phase 1
- **No thread safety:** Out of scope for console app; add locks in Phase 2 if needed

---

## 4. Module Design

### Module Responsibility Matrix

| Module | Responsibilities | Public API | Dependencies |
|--------|------------------|------------|--------------|
| `models.task` | Data structure, validation | `Task`, `TaskStatus` | stdlib only |
| `storage.in_memory` | CRUD primitives, ID management | `InMemoryStorage.{add,get,update,delete,list_all}` | `models.task` |
| `operations.task_operations` | Business logic, filtering | `TaskOperations.{add_task,mark_complete,delete_task,list_tasks}` | `storage`, `models` |
| `ui.menu` | Menu display, input parsing | `display_menu()`, `get_user_choice()` | stdlib only |
| `ui.display` | Task formatting, output | `format_task()`, `print_tasks()` | `models.task` |
| `main` | Application loop, orchestration | `main()` | All UI + operations |

### Public APIs

**storage/in_memory.py:**
```python
class InMemoryStorage:
    def add(self, title: str) -> Task: ...
    def get(self, task_id: int) -> Task | None: ...
    def update(self, task_id: int, **kwargs) -> Task: ...
    def delete(self, task_id: int) -> bool: ...
    def list_all(self) -> list[Task]: ...
```

**operations/task_operations.py:**
```python
class TaskOperations:
    def add_task(self, title: str) -> Task: ...
    def mark_complete(self, task_id: int) -> Task: ...
    def delete_task(self, task_id: int) -> bool: ...
    def list_tasks(self) -> list[Task]: ...
    def filter_by_status(self, status: TaskStatus) -> list[Task]: ...
```

**ui/display.py:**
```python
def format_task(task: Task) -> str: ...
def print_tasks(tasks: list[Task], title: str = "Tasks") -> None: ...
```

---

## 5. UI/UX Flow

### Menu System Design

```
┌─────────────────────────────────────┐
│       Todo App - Main Menu          │
├─────────────────────────────────────┤
│ 1. Add Task                         │
│ 2. View All Tasks                   │
│ 3. View Pending Tasks               │
│ 4. View Completed Tasks             │
│ 5. Mark Task Complete               │
│ 6. Delete Task                      │
│ 0. Exit                             │
└─────────────────────────────────────┘
Enter choice:
```

### Input/Output Handling

**Input Flow:**
```
User Input → Strip whitespace → Validate type → Validate constraints → Return or re-prompt
```

**Error Display Strategy:**
```
❌ Error: Title must be 1-200 characters (got 0)

❌ Task not found: ID 99

✓ Task added: "Buy groceries" (ID: 1)
```

**Task Display Format:**
```
[1] Buy groceries [PENDING]
    Created: 2025-01-15T10:30:00

[2] Call dentist [COMPLETED]
    Created: 2025-01-14T09:00:00
    Completed: 2025-01-15T11:45:00
```

---

## 6. Testing Strategy

### Unit Test Structure

```
tests/unit/
├── test_task.py
│   ✓ test_task_creation_valid
│   ✓ test_task_validation_title_empty
│   ✓ test_task_validation_title_too_long
│   ✓ test_status_enum_values
│   ✓ test_completed_task_requires_timestamp
├── test_storage.py
│   ✓ test_add_task_generates_id
│   ✓ test_get_task_existing
│   ✓ test_get_task_nonexistent
│   ✓ test_update_task_status
│   ✓ test_delete_task_success
│   ✓ test_list_all_empty
│   ✓ test_list_all_multiple
└── test_operations.py
    ✓ test_add_task_valid_title
    ✓ test_mark_complete_existing_task
    ✓ test_mark_complete_nonexistent_task
    ✓ test_delete_task_nonexistent
    ✓ test_list_tasks_by_status
```

### Integration Test Scenarios

```
tests/integration/test_workflows.py
✓ test_full_task_lifecycle (add → view → mark_complete → delete)
✓ test_multiple_operations_independence
✓ test_id_generation_monotonic
✓ test_status_filter_correctness
```

### Coverage Targets

- **Overall:** 90%+ line coverage
- **Critical paths:** 100% (add, mark_complete, delete)
- **Error paths:** 85%+ (all ValueError, KeyError paths)
- **UI layer:** 70%+ (input parsing, display logic)

**Coverage Tools:** `pytest-cov` via UV

---

## 7. Error Handling Strategy

### Exception Hierarchy

```python
class TodoAppError(Exception):
    """Base exception for todo app errors."""
    pass

class ValidationError(TodoAppError):
    """Invalid input or constraint violation."""
    pass

class NotFoundError(TodoAppError):
    """Requested resource does not exist."""
    pass
```

### Validation Layer

```
Input → UI Layer (basic type checks) → Operations Layer (business rules) → Storage Layer (data integrity)
```

**Validation Rules:**
- UI: Non-empty strings, valid menu choices (0-6)
- Operations: Title length (1-200), task existence, status transitions
- Storage: ID uniqueness, data consistency

### Recovery Flows

```python
# Example: Add Task Flow
try:
    title = input("Enter task title: ").strip()
    if not title:
        raise ValidationError("Title cannot be empty")
    task = operations.add_task(title)
    print(f"✓ Task added: \"{task.title}\" (ID: {task.id})")
except ValidationError as e:
    print(f"❌ Error: {e}")
    # Return to menu, do not crash
```

**Principle:** Never crash the app on user error; always return to main menu.

---

## 8. Key Design Decisions

### Decision 1: Dict[int, Task] over List[Task]

**Options Considered:**
1. List with linear search
2. Dict with integer keys
3. Dict with UUID keys

**Trade-offs:**
- List: O(n) lookup, simpler code
- Dict[int]: O(1) lookup, requires ID counter
- Dict[UUID]: O(1) lookup, overkill for Phase 1

**Rationale:** Dict[int] chosen for O(1) performance in filter/search operations. Auto-increment IDs sufficient for single-user console app; UUIDs add complexity without benefit.

### Decision 2: In-Memory Storage for Phase 1

**Options Considered:**
1. SQLite database
2. JSON file persistence
3. In-memory only

**Trade-offs:**
- SQLite: Overkill, adds dependency, complicates testing
- JSON: Requires file I/O, error handling, slower tests
- In-memory: Fast, simple, meets spec

**Rationale:** Spec explicitly scopes Phase 1 to in-memory. Persistence deferred to Phase 2 (SQLite). This enables faster iteration and simpler TDD.

### Decision 3: No External CLI Frameworks

**Options Considered:**
1. Click/Typer for CLI
2. Rich for formatting
3. Raw input()/print()

**Trade-offs:**
- Click: Better UX, more dependencies, steeper learning curve
- Rich: Beautiful output, 15+ dependencies, bloat
- Raw: Zero dependencies, basic but functional

**Rationale:** Spec constraint (no external CLI frameworks). Raw I/O sufficient for console app; keeps codebase minimal and portable.

### Decision 4: Dataclasses with slots=True

**Options Considered:**
1. Plain classes with __init__
2. Dataclasses (default)
3. Dataclasses with slots=True

**Trade-offs:**
- Plain classes: More boilerplate, no type hints by default
- Dataclasses: Less boilerplate, type hints, __eq__/__repr__ free
- Dataclasses + slots: 30% memory savings, faster attribute access

**Rationale:** Python 3.13 supports `slots=True` in dataclasses. Minimal code change for measurable performance gain. Type hints enforce correctness at design time.

---

## 9. Performance Considerations

### Memory Management

**Current:** In-memory Dict[int, Task]
- **Best case:** 1000 tasks ≈ 200KB (with slots)
- **Worst case:** 10,000 tasks ≈ 2MB
- **Phase 1 target:** <1000 tasks (reasonable for console app)

**Optimization Opportunity (Phase 2):** Implement pagination if task count exceeds 1000.

### Complexity Analysis

| Operation | Time Complexity | Space Complexity |
|-----------|----------------|------------------|
| Add Task | O(1) | O(1) |
| Get Task (by ID) | O(1) | O(1) |
| Update Task | O(1) | O(1) |
| Delete Task | O(1) | O(1) |
| List All | O(n) | O(n) |
| Filter (by status) | O(n) | O(k) where k = matches |

**Critical Path:** Filtering is O(n) but unavoidable without indexing. For Phase 1 (<1000 tasks), <10ms latency expected.

### Optimization Opportunities (Phase 2+)

1. **Status Index:** Maintain separate Dict[TaskStatus, Set[int]] for O(1) status filtering
2. **Full-Text Search:** Use inverted index for keyword filtering (O(k) lookup instead of O(n))
3. **LRU Cache:** Cache recent get() calls if read-heavy workload

**Decision:** Defer optimizations until Phase 2 profiling confirms bottlenecks.

---

## 10. Deployment Instructions

### Setup

**Prerequisites:**
- Python 3.13+ installed
- UV package manager installed

**Steps:**
```bash
# 1. Verify Python version
python --version  # Must show 3.13+

# 2. Navigate to project directory
cd hack2phase1

# 3. Create virtual environment with UV
uv venv

# 4. Activate environment
# Windows: .venv\Scripts\activate
# Linux/Mac: source .venv/bin/activate

# 5. Install project in editable mode
uv pip install -e .

# 6. Install dev dependencies
uv pip install -e ".[dev]"
```

### Run Command

```bash
# Development mode (with type checking)
python -m todo.main

# Production mode (optimized)
python -OO -m todo.main
```

### Development vs Production

**Development:**
- Assertions enabled (`-O` flag NOT used)
- Debug logging to console
- Type hints checked: `uv run mypy src/ --strict`
- Tests run: `uv run pytest tests/ --cov=src/todo --cov-report=term-missing`

**Production:**
- Assertions disabled (`-OO` flag)
- No debug output
- Performance profiling: `python -m cProfile -o profile.stats -m todo.main`

---

## 11. Quality Gates

**All must pass before code merge:**

```bash
# Type checking
uv run mypy src/ --strict

# Linting
uv run flake8 src/ --max-line-length=100

# Tests and coverage
uv run pytest tests/ --cov=src/todo --cov-report=term-missing -v
# Must show: ≥90% coverage, all tests passing

# Code style
uv run black --check src/
```

---

## 12. Next Steps

1. **Create Task Breakdown** → `specs/phase-1/tasks.md` (decompose plan into testable TDD tasks)
2. **Set Up UV Project** → `pyproject.toml`, create module structure
3. **Implement Data Model** → `src/todo/models/task.py` with full unit tests
4. **Begin Red-Green-Refactor** → Follow TDD cycle for each task

---

## Architectural Decision Records (ADRs)

📋 **ADR 1: Dict[int, Task] Storage**
- **Status:** Suggested for documentation
- **Context:** Need O(1) task lookup by ID
- **Decision:** Use Dict[int, Task] with auto-increment counter
- **Consequences:** No ID reuse; requires counter management; Phase 2 migration to SQLite straightforward
- **Alternatives Rejected:** List (O(n) lookups); UUID keys (overkill)

📋 **ADR 2: In-Memory Storage Phase 1**
- **Status:** Suggested for documentation
- **Context:** Spec Phase 1 constraint: no persistence
- **Decision:** In-memory Dict only; persistence deferred to Phase 2
- **Consequences:** Data loss on exit (expected); fast tests; simple TDD
- **Alternatives Rejected:** SQLite (too much scope); JSON file (I/O overhead)

---

**Plan Ready for Implementation.** All sections derived from spec, provide clear technical path, and enable TDD. Next: Task breakdown and code development.
