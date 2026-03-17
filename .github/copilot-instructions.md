# FastAPI Project Development Guidelines

This repository follows **Onion Architecture** and strict development standards.
All generated code must follow the rules defined below.

---

# Tech Stack

- Python 3.12+
- FastAPI
- Async programming (async/await)
- SQLAlchemy 2.0 (Async ORM)
- Pydantic v2
- PostgreSQL
- Alembic for migrations
- Pytest for testing
- Docker for containerization

---

# Architecture Pattern

This project follows **Onion Architecture**.

Layer dependency rule:

# Need to check, may be to follows the architecture strictlty, we can have some exceptions for some cases, but in general, we should follow this rule.
Outer layers depend on inner layers only.

# General Coding Rules

All code must follow:

- **PEP8**
- **Type hints required**
- **Async-first design**
- **Single responsibility principle**
- **Dependency injection**

Formatting rules:

- Use `ruff` for linting
- Use `black` for formatting
- Max line length: 88
- Use `is` for None checks


