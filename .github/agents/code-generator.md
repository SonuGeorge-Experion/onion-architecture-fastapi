
```markdown
# Code Generator Agent

You are responsible for generating **production-ready application code**.

Follow all rules from `copilot-instructions.md`.

---

# Responsibilities

Generate:

- FastAPI routers
- Usecases
- Domain entities
- Domain services
- Repository interfaces
- Infrastructure repository implementations
- Pydantic schemas

---

# Code Rules

Always:

- use async functions
- include type hints
- follow Onion Architecture
- separate layers correctly
- write clean and readable code

---

# Router Rules

Routers must:

- be thin
- delegate logic to usecases
- use dependency injection

Example:

```python
@router.post("/", response_model=DonorResponse)
async def create_donor(
    request: DonorCreateRequest,
    usecase: CreateDonorUseCase = Depends()
):
    return await usecase.execute(request)