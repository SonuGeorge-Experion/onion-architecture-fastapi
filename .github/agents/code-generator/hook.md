# Code Generator Agent Hook

This hook coordinates all instructions required for the Code Generator Agent.

The agent must read and apply instructions from the following files in order.

---

# Step 1 — Load Global Project Instructions

Load:

.github/copilot-instructions.md

This file defines:

- coding standards
- architecture rules
- security practices
- project folder structure
- FastAPI conventions
- SQLAlchemy conventions

These rules must always be enforced.

---

# Step 2 — Load Code Generator Agent Definition

Load:

.github/agents/code-generator.md

This file defines:

- responsibilities of the code generator
- allowed actions
- forbidden patterns
- architecture boundaries

---

# Step 3 — Load Core Prompt

Load:

.github/agents/code-generator/prompt.md

This prompt defines:

- base behavior
- code generation style
- documentation requirements
- error handling standards

---

# Step 4 — Load Specialized Prompts

Depending on the requested task, load one or more specialized prompts.

Available prompts:

.github/agents/code-generator/prompts/api_generation.md  
.github/agents/code-generator/prompts/usecase_generation.md  
.github/agents/code-generator/prompts/domain_generation.md  
.github/agents/code-generator/prompts/repository_generation.md  
.github/agents/code-generator/prompts/sqlalchemy_generation.md

---

# Prompt Selection Rules

If request involves:

API endpoints  
→ load api_generation.md

Application orchestration  
→ load usecase_generation.md

Domain entities or services  
→ load domain_generation.md

Database repository logic  
→ load repository_generation.md

SQLAlchemy models or queries  
→ load sqlalchemy_generation.md

Multiple prompts may be combined.

---

# Architecture Enforcement

The agent must ensure the following:

API layer:
- contains routers only
- no business logic
- uses dependency injection

Application layer:
- usecases orchestrate domain operations

Domain layer:
- contains entities
- contains value objects
- contains domain services
- no framework dependencies

Infrastructure layer:
- contains SQLAlchemy models
- implements repositories

---

# Async Enforcement

All generated code must support async execution.

Requirements:

- async FastAPI endpoints
- async SQLAlchemy usage
- async repository methods

Blocking calls must never be used.

---

# Security Enforcement

Generated code must enforce:

- input validation using Pydantic
- parameterized SQL queries
- no secrets in logs
- no raw SQL injection risk

---

# Performance Enforcement

Agent must prevent:

- N+1 database queries
- inefficient ORM loading

Prefer:

- select() syntax
- indexed filters
- pagination for large datasets

---

# Documentation Requirement

Generated code must include:

- type hints
- docstrings
- clear function naming

---

# Post-Generation Hook

After generating code:

1. Verify architecture compliance
2. Ensure imports are correct
3. Ensure async usage
4. Ensure type hints exist
5. Ensure PEP8 compliance

---

# Test Generation Trigger

After code generation completes:

Trigger the Test Generator Agent.

The test generator must create:

- unit tests
- API tests
- repository tests