# Claude Code - Phase I Todo App Development Guide

**Project:** Todo In-Memory Python Console Application
**Status:** Phase I - Specification & Planning Complete
**Date:** 2025-12-28

---

## Quick Start

### Prerequisites
- Python 3.13+
- UV package manager ([install](https://astral.sh/uv/install.sh))

### Run the Application (After Implementation)

```bash
# Setup (one-time)
cd hack2phase1
uv sync

# Run
uv run python -m todo.main
```

### Run Tests

```bash
# All tests
uv run pytest tests/ -v

# With coverage
uv run pytest tests/ --cov=src/todo --cov-report=term-missing

# Unit tests only
uv run pytest tests/unit/ -v

# Integration tests only
uv run pytest tests/integration/ -v
```

### Code Quality Checks

```bash
# Type checking (strict mode)
uv run mypy src/todo --strict

# Linting
uv run flake8 src/todo --max-line-length=100

# All checks
./verify-quality.sh  # (to be created in Phase I)
```

---

## Project Structure

```
hack2phase1/
├── .claude/                           # Claude Code configuration
│   ├── skills/                        # Reusable skill definitions
│   │   ├── spec-analyzer.md           # Validate specs against Nine Pillars
│   │   ├── python-expert.md           # Implement clean Python 3.13
│   │   └── README.md                  # Skills registry
│   └── agents/                        # Agent definitions
│       ├── system-architect.md        # Planning agent
│       ├── python-developer.md        # Implementation agent
│       └── todo-evolution-architect.md # Orchestration agent
├── src/                               # Application source code
│   └── todo/
│       ├── __init__.py
│       ├── main.py                    # Entry point
│       ├── models/
│       │   ├── __init__.py
│       │   └── task.py                # Task dataclass
│       ├── storage/
│       │   ├── __init__.py
│       │   └── in_memory.py           # Storage backend
│       ├── operations/
│       │   ├── __init__.py
│       │   └── task_operations.py     # Business logic
│       └── ui/
│           ├── __init__.py
│           ├── menu.py                # Interactive menu
│           └── display.py             # Display formatting
├── tests/                             # Test suite
│   ├── unit/                          # Unit tests
│   │   ├── test_task.py
│   │   ├── test_storage.py
│   │   └── test_operations.py
│   └── integration/                   # Integration tests
│       ├── test_workflows.py
│       └── test_full_application.py
├── specs/                             # Specifications & Plans
│   └── phase-1/
│       ├── spec.md                    # Feature specification (COMPLETED)
│       ├── plan.md                    # Architecture plan (COMPLETED)
│       └── tasks.md                   # Task breakdown (COMPLETED)
├── specs-history/                     # Archived specifications
│   └── phase-1-todo-spec.md           # Original spec document
├── history/                           # Development records
│   ├── prompts/
│   │   ├── constitution/              # Constitution-related PRs
│   │   ├── phase-1/                   # Phase 1 PRs
│   │   └── general/                   # General PRs
│   └── adr/                           # Architectural Decision Records
├── .specify/                          # Spec Framework
│   ├── memory/
│   │   └── constitution.md            # Project constitution (COMPLETED)
│   └── templates/
├── pyproject.toml                     # Project configuration (TO CREATE)
├── README.md                          # Project documentation
└── CLAUDE.md                          # This file

```

---

## Development Workflow

### Phase I: In-Memory Console App (Current)

**Status:** Specification ✅ → Architecture Planning ✅ → Task Breakdown ✅ → **Implementation (Next)**

#### Completed Artifacts

1. **Constitution** (`.specify/memory/constitution.md`)
   - 6 core principles (SDD, Test-First, Clean Code, Agentic Stack, MVP Scope, UV)
   - Code quality standards (type hints, testing, style, observability)
   - Development workflow (spec→plan→tasks→TDD→review)
   - Performance targets, reliability requirements, security standards
   - Version 1.1.0 (ratified 2025-12-28)

2. **Specification** (`specs-history/phase-1-todo-spec.md`)
   - 5 core features (Add, View, Update, Delete, Complete)
   - Data model with Task entity and validation rules
   - 6 detailed user workflows (add/list/update/delete/complete)
   - Error taxonomy with 5 edge cases
   - 31 testable acceptance criteria
   - Non-functional requirements (performance, reliability, security, maintainability)
   - Constraints and assumptions documented
   - Version 1.0 (complete, ready for architecture)

3. **Architecture Plan** (`specs/phase-1/plan.md`)
   - Layered architecture (UI → Operations → Storage → Models)
   - 12 sections covering design, modules, testing, error handling
   - Directory structure with all source files specified
   - Data model with Task dataclass (slots=True for efficiency)
   - Module responsibility matrix and public APIs
   - Testing strategy with unit/integration breakdown
   - Exception hierarchy and validation layers
   - 4 key design decisions with rationale (Dict vs List, in-memory, no frameworks, dataclasses)
   - Performance analysis (O(n) complexity, memory budgets)
   - Deployment and quality gates
   - 2 ADR suggestions for documentation
   - Version 1.0 (complete, ready for implementation)

4. **Task Breakdown** (`specs/phase-1/tasks.md`)
   - 23 granular, dependency-ordered tasks
   - 7 implementation categories:
     - Project Setup (5 tasks)
     - Data Models (3 tasks)
     - Storage Layer (3 tasks)
     - Operations Layer (4 tasks)
     - UI Layer (3 tasks)
     - Main Application (2 tasks)
     - Quality Assurance (3 tasks)
   - Every task includes:
     - ID (T-001 to T-023)
     - Complexity (Simple/Medium/Complex)
     - Estimated duration (<2 hours each)
     - Dependencies (for proper ordering)
     - GIVEN/WHEN/THEN acceptance criteria
     - TDD workflow guidance
     - Spec/plan cross-references
   - Total estimated duration: 34.5 hours
   - Quality gates: ≥90% coverage, strict type checking, performance benchmarks
   - Acceptance checklist for Phase I completion
   - Version 1.0 (complete, ready for development)

#### Next Step: Implementation

**To begin Phase I implementation:**

1. **Start with Task T-001** (Project Setup):
   ```bash
   # Create pyproject.toml, directory structure
   # Configure UV, pytest, mypy, flake8
   ```

2. **Follow TDD Discipline:**
   - **Red:** Write tests first (failing)
   - **Green:** Implement to pass tests
   - **Refactor:** Optimize after green

3. **Track Progress:**
   - Complete tasks in order (respect dependencies)
   - Verify all acceptance criteria pass before marking complete
   - Run full test suite after each task: `uv run pytest`

4. **Quality Gates:**
   - Type checking: `uv run mypy src/todo --strict`
   - Linting: `uv run flake8 src/todo --max-line-length=100`
   - Coverage: `uv run pytest --cov` (≥90% target)

---

## Agents & Skills

### Available Agents

1. **system-architect**
   - Planning and architecture design
   - Creates specifications, plans, design documents
   - Usage: For planning tasks and architectural decisions

2. **python-developer**
   - Implementation of Python code
   - Manages UV dependencies, runs tests
   - Usage: For code implementation and testing

3. **todo-evolution-architect**
   - Orchestrates full lifecycle of Todo app evolution
   - Coordinates across planning and implementation phases
   - Usage: For multi-phase coordination and major decisions

### Available Skills

1. **spec-analyzer** (`.claude/skills/spec-analyzer.md`)
   - Validates specifications against Nine Pillars criteria
   - Usage: Analyze specs before planning phase

2. **python-expert** (`.claude/skills/python-expert.md`)
   - Implements clean Python 3.13 code using UV
   - Type hints, testing, quality gates
   - Usage: Code implementation tasks

---

## Key Principles (From Constitution)

### I. Spec-Driven Development
- Every feature begins with explicit, testable specification
- Specifications are source of truth
- All artifacts derive from specification

### II. Test-First (NON-NEGOTIABLE)
- Red-Green-Refactor cycle mandatory
- Tests written first, then implementation
- Ensures requirements objectively met

### III. Clean Code Standards
- Strict type hints (mypy --strict)
- PEP 8 compliance (flake8)
- Modular, single-purpose functions
- 100% type hint coverage

### IV. Agentic Development Stack
- Specialized agents for planning and implementation
- MCP tools and CLI commands as primary interfaces
- Prompt History Records (PHRs) for traceability
- ADRs for significant decisions

### V. Minimal Viable Scope
- Phase I: In-memory only (no persistence)
- 5 core features, nothing more
- Foundation for Phase 2 (SQLite persistence)

### VI. Dependency Management via UV
- UV exclusively (no pip, poetry, pipenv)
- Minimal runtime dependencies (stdlib only)
- Development tools managed separately

---

## Performance Targets (Phase I)

- **Task Addition:** < 10ms p95
- **Task Listing (1000 tasks):** < 50ms p95
- **Memory (10,000 tasks):** < 50MB
- **Startup Time:** < 100ms
- **Code Coverage:** ≥ 90%
- **Type Coverage:** 100% (mypy strict)

---

## Files to Create (Phase I)

During implementation, the following new files will be created:

```
src/todo/
├── __init__.py                        # Module exports
├── main.py                            # Entry point
├── models/
│   ├── __init__.py
│   └── task.py                        # Task dataclass (~150 lines)
├── storage/
│   ├── __init__.py
│   └── in_memory.py                   # Storage backend (~200 lines)
├── operations/
│   ├── __init__.py
│   └── task_operations.py             # Business logic (~300 lines)
└── ui/
    ├── __init__.py
    ├── menu.py                        # Menu system (~250 lines)
    └── display.py                     # Display formatting (~150 lines)

tests/
├── __init__.py
├── unit/
│   ├── __init__.py
│   ├── test_task.py                   # Model tests (~400 lines)
│   ├── test_storage.py                # Storage tests (~350 lines)
│   └── test_operations.py             # Operations tests (~500 lines)
└── integration/
    ├── __init__.py
    ├── test_workflows.py              # Workflow tests (~300 lines)
    └── test_full_application.py       # Full integration (~400 lines)

pyproject.toml                         # Project config (~50 lines)
README.md                              # Documentation (~150 lines)
```

**Total New Code:** ~3,500 lines (implementation + tests)

---

## Prompt History Records (PHRs)

Development is tracked in Prompt History Records for traceability:

```
history/prompts/
├── constitution/
│   └── (constitution updates)
├── phase-1/
│   └── 001-phase-1-task-breakdown.tasks.prompt.md
├── general/
│   ├── 001-phase-1-todo-spec-creation.general.prompt.md
│   └── 002-phase-1-architecture-plan.general.prompt.md
└── (future phases)

history/adr/
├── (to be created as significant decisions emerge)
```

---

## Constitutional Compliance Checklist

As you implement, ensure:

- [ ] All code has type hints (mypy --strict passes)
- [ ] PEP 8 compliance verified (flake8 passes)
- [ ] Tests written first (TDD discipline)
- [ ] ≥90% test coverage achieved
- [ ] Error handling tested (all error paths)
- [ ] Performance meets targets (<10ms add, <50ms list)
- [ ] No hardcoded secrets or configuration
- [ ] Module boundaries respect architecture plan
- [ ] Imports follow hierarchy (UI→Ops→Storage→Models)
- [ ] Documentation complete (docstrings, README)

---

## Common Commands

### Development Setup
```bash
# Clone/navigate to project
cd hack2phase1

# Create virtual environment
uv sync

# Install dev dependencies
uv pip install -e ".[dev]"
```

### Running Application
```bash
# Interactive console app
uv run python -m todo.main

# Production optimized
uv run python -OO -m todo.main
```

### Testing
```bash
# Run all tests
uv run pytest tests/ -v

# With coverage report
uv run pytest tests/ --cov=src/todo --cov-report=html

# Run specific test file
uv run pytest tests/unit/test_task.py -v

# Run specific test
uv run pytest tests/unit/test_task.py::test_task_creation_valid -v
```

### Code Quality
```bash
# Type checking
uv run mypy src/todo --strict

# Linting
uv run flake8 src/todo --max-line-length=100

# Code formatting check
uv run black --check src/todo

# All checks combined
uv run mypy src/todo --strict && \
uv run flake8 src/todo --max-line-length=100 && \
uv run pytest tests/ --cov=src/todo --cov-fail-under=90
```

### Debugging
```bash
# Run with debug output
PYTHONUNBUFFERED=1 uv run python -m todo.main

# Profile performance
uv run python -m cProfile -o profile.stats -m todo.main

# View coverage report
uv run pytest --cov=src/todo --cov-report=html
open htmlcov/index.html  # macOS
# or
start htmlcov/index.html  # Windows
```

---

## Troubleshooting

### Python Version Issues
```bash
# Verify Python 3.13+
python --version

# Use UV to switch versions
uv python list
uv python install 3.13
```

### UV Sync Failures
```bash
# Clear cache and resync
uv cache clean
uv sync --upgrade
```

### Import Errors
```bash
# Reinstall editable mode
uv pip install -e .

# Verify PYTHONPATH
echo $PYTHONPATH  # (should include src/)
```

### Test Failures
```bash
# Run with verbose output
uv run pytest tests/ -vv --tb=long

# Run single test with pdb
uv run pytest tests/unit/test_task.py::test_name --pdb
```

---

## Phase II Planning (Future)

After Phase I is complete, Phase II will add:
- SQLite persistence layer
- Data migration from in-memory
- File I/O and error handling
- Backup/restore functionality

Architecture is designed for this migration:
- Storage layer can be swapped (Interface pattern)
- Models remain unchanged
- Operations layer provides stable API

---

## Support & Feedback

### Getting Help
- Run `/help` for Claude Code CLI help
- Review `.specify/memory/constitution.md` for principles
- Check `specs/phase-1/plan.md` for architecture details
- Refer to `specs/phase-1/tasks.md` for task specifics

### Reporting Issues
- File issues at: https://github.com/anthropics/claude-code/issues
- Include context: spec/plan section references
- Provide repro steps from task acceptance criteria

---

## Document Version History

| Component | Version | Date | Status |
|-----------|---------|------|--------|
| Constitution | 1.1.0 | 2025-12-28 | ✅ Approved |
| Specification | 1.0 | 2025-12-28 | ✅ Complete |
| Architecture Plan | 1.0 | 2025-12-28 | ✅ Complete |
| Task Breakdown | 1.0 | 2025-12-28 | ✅ Ready |
| Implementation | TBD | TBD | ⏳ In Progress |

---

**Last Updated:** 2025-12-28
**Next Milestone:** Begin Phase I Implementation (T-001: Project Setup)
