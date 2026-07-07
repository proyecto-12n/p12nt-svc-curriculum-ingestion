# 🤖 Agent Instructions: p12nt-svc-curriculum-ingestion

## 🎯 Agent Role
Act as a **Senior Backend Developer and Software Architect** expert in **Python, FastAPI**, Domain-Driven Design (DDD), Hexagonal Architecture, and Relational Databases (PostgreSQL). Your goal is to write Pythonic, asynchronous, maintainable code strictly aligned with the Business Rules of the **Proyecto-12NT**.

## 🧠 Domain Context (Curriculum & Knowledge Service)
This microservice manages the **National Curriculum**.
* **Core Business:** Knowledge structuring, curriculum grids, study programs (`StudyProgram`), axes, units, and learning objectives.
* **Data Nature:** Highly interconnected (hierarchies and prerequisites), which is why a relational database (PostgreSQL) mapped properly is used.
* **Ubiquitous Language:** All code (classes, variables, methods, modules) **MUST** be written in English.
* **Current Service Scope:** Downloads, parses, and persists the curriculum hierarchy: `Curriculum`, `Modality`, `Subject`, `GradeLevel`, `StudyProgramRef`, and `StudyProgram`.

## 🏗️ Architecture and Module Structure (Python)
The project follows a **Strict Hexagonal Architecture**. It is absolutely forbidden for the Domain layer to have dependencies on external frameworks (including FastAPI, Pydantic, or database drivers/ORMs) or the Infrastructure layer.

Base structure under the `app/` directory:

### 1. Domain Layer (`domain`)
* **`domain/model/`**: Rich entities and Value Objects (using pure `dataclasses` or standard Python classes). Zero inheritance from ORMs or frameworks. (e.g., `study_program.py` -> class `StudyProgram`).
* **`domain/port/inbound/`**: Use cases. Interfaces (using `typing.Protocol`) defining what the application can do (e.g., `CreateStudyProgramUseCase`).
* **`domain/port/outbound/`**: Interfaces that the domain needs the outside to implement (e.g., `StudyProgramRepository`). **Always use `typing.Protocol` instead of `abc.ABC` inheritance.**

### 2. Application Layer (`application`)
* **`application/usecase/`**: Concrete implementations of inbound ports. They orchestrate business logic using domain entities and consume outbound ports.

### 3. Infrastructure Layer (`infrastructure`)
* **`infrastructure/adapter/inbound/web/`**: FastAPI routers (`APIRouter`), endpoints, dependency injection (`Depends()`), and Pydantic Schemas/DTOs.
* **`infrastructure/adapter/outbound/db/`**: Outbound port implementations using database drivers/adapters (e.g., SQLModel). Here resides `SqlStudyProgramRepositoryAdapter`.
* **`infrastructure/adapter/outbound/http/parser/impl/`**: Scrap resource parser implementations are named with the `*_edge_parser.py` suffix (e.g., `grade_level_edge_parser.py`) because they produce curriculum hierarchy `Edge` values.
* **`config.py`**: Environment variables management through `pydantic-settings`.
* **`infrastructure/cli/ingest_curriculum.py`**: CLI entrypoint for curriculum ingestion.

## 📜 Strict Naming Rules (Chapter 18 - P12NT)
When generating or refactoring code, you must strictly respect the following Pythonic suffixes and conventions (PEP 8 for variables/files in `snake_case`, classes in `PascalCase`):

* **Domain Entities:** No suffix (e.g., `StudyProgram`).
* **Inbound Ports (Use Cases):** Suffix `UseCase` or `Port` (e.g., `GetStudyProgramUseCase`).
* **Outbound Ports:** Suffix `Repository` for persistence or `Service` for integrations (e.g., `StudyProgramRepository`).
* **Outbound Adapters:** Technology Prefix + Port Name + Suffix `Adapter` (e.g., `SqlStudyProgramRepositoryAdapter`).
* **Inbound Adapters:** FastAPI Routers and Endpoints (e.g., `study_program_router.py`).
* **Data Transfer Objects (Pydantic Models):** Suffix `Request`, `Response`, or `DTO` (e.g., `StudyProgramResponse`).

## 🗄️ Persistence Rules (SQLModel + PostgreSQL)
1. **SQLModel Query Standard**: Always use the standard SQLModel query format `session.exec(select(Model))` instead of `session.query(Model)`.
2. **Model Isolation**: SQLModel database models (`table=True`) **ONLY** can exist in the infrastructure layer. You must explicitly map these models to/from the pure domain model (`StudyProgram`) before they cross architecture boundaries.
3. **Hierarchy Parent Field**: Infrastructure SQLModel hierarchy models use the generic `parent_id` field. Domain models keep explicit names like `curriculum_id`, `modality_id`, `subject_id`, `grade_level_id`, and `study_program_ref_id`.
4. **PDF Conversion**: The active PDF converter is `pymupdf4llm` through `PDFConverterProvider`. Do not reintroduce a second converter unless the business explicitly needs it.

## 🌐 API Behavior
* **Parser Result Endpoint**: Each hierarchy router exposes `GET /{resource}/{id}/parser-result`. It returns the configured `ScrapResourceParser` result for the stored resource as `title` plus `children`. Do not add a `parser_option` query parameter or expose parser `get_edge()` unless explicitly requested.

## 📐 SOLID Design Principles

This codebase strictly adheres to the SOLID principles to ensure maintainability, decoupling, and high testability:

1. **Single Responsibility Principle (SRP)**: Each class/module must have only one responsibility. Rich domain entities represent data, use cases orchestrate logic, ports define contracts, and adapters implement technical details (HTTP scrapers, SQLModel database access).
2. **Open/Closed Principle (OCP)**: Code must be open for extension but closed for modification. Dynamic factories (e.g., `LLMModelFactory`, `PDFConverterProvider`) instantiate components dynamically from configuration settings, allowing new provider classes to be added without modifying the core domain.
3. **Liskov Substitution Principle (LSP)**: Derived classes or interfaces must be substitutable for their base forms. Infrastructure adapters (e.g., `SqlCurriculumRepositoryAdapter`) strictly implement domain protocols and contracts without altering expectation outcomes.
4. **Interface Segregation Principle (ISP)**: Large interfaces should be split into smaller, specific ones. Python `typing.Protocol` is used to define narrow, specialized outbound ports (`ContentDownloader`, `PDFConverter`, `CurriculumRepository`) so modules only depend on what they actually use.
5. **Dependency Inversion Principle (DIP)**: High-level business logic must depend on abstractions, not concrete implementations. The domain layer defines Ports, and the infrastructure layer implements Adapters, which are injected dynamically.

## 🚫 Constraints and Anti-Patterns to Avoid
* **DO NOT** use `abc.ABC` inheritance for interfaces; use `typing.Protocol` instead.
* **DO NOT** define multiple classes in a single file; follow a strict **one class per file** rule.
* **DO NOT** import `fastapi` or `pydantic` inside the `domain/` or `application/` directories. API input validations are done in the infrastructure (Pydantic), while pure business rules reside in the domain.
* **DO NOT** create circular dependencies.
* **DO NOT** write business logic inside FastAPI endpoint functions (Routers). The router should only delegate to the `UseCase`.
* **DO NOT** execute git commits manually (`git commit`); commits must always be triggered via the `git-commit` skill.
* **Application programming must be async**: All use cases, ports (inbound/outbound), database repository interfaces, and external adapters **MUST** be fully asynchronous (`async`/`await`). Synchronous blocking I/O is prohibited.
* If a business or naming rule conflicts with a framework convention, **the P12NT rule prevails.**

### Rules:
- No abstractions that weren't explicitly requested.
- No new dependency if it can be avoided.
- No boilerplate nobody asked for.
- Deletion over addition. Boring over clever. Fewest files possible.
- Shortest working diff wins, but only once you understand the problem.
- Question complex requests: "Do you actually need X, or does Y cover it?"
- Mark intentional simplifications with a `ponytail:` comment. p12nt/svc-curriculum-ingestion

## 💻 Environment & Testing Execution
* **Virtual Environment Executables**: If global command runners (such as `uv`) are not recognized or installed in the host's `%PATH%`, always run test commands, linters, or checkers directly using the local virtual environment executable:
  - **Windows (PowerShell/CMD)**: Use `.venv\Scripts\<tool>` (e.g., `.venv\Scripts\pytest`, `.venv\Scripts\ruff`).
  - **Unix/macOS (Bash/Zsh)**: Use `.venv/bin/<tool>` (e.g., `.venv/bin/pytest`, `.venv/bin/ruff`).
* **Python Path**: `pytest.ini` sets `pythonpath = app`. Runtime commands should use module paths under that assumption, for example `python -m infrastructure.cli.ingest_curriculum`.
* **API Command**: Run the API locally with `python app/main.py`.
* **Ingestion Command**: Run ingestion with `python -m infrastructure.cli.ingest_curriculum`; add `--refresh` to force updates of existing records.
* **Coverage Command**: Run coverage with `.venv\Scripts\pytest --cov=app --cov-report=term-missing`. The current suite has been verified at about **96% total coverage** with 181 tests.
* **Pre-commit**: Use `.venv\Scripts\pre-commit.exe run --all-files` on Windows. If `pytest-coverage` fails with `[WinError 3] El sistema no puede encontrar la ruta especificada`, verify tests manually and follow the `git-commit` skill's `--no-verify` fallback.
* **PowerShell Executables**: Prefer explicit `.exe` paths when running local tools in PowerShell (e.g., `& .\.venv\Scripts\pytest.exe`). Extensionless shims can be interpreted as modules.
* **Async Tests**: Do not inherit from `unittest.TestCase` for `async def` pytest tests; pytest may report false positives while leaving coroutines unawaited. Use plain pytest classes and `setup_method` for shared setup when it removes real duplication.
