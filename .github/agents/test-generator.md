
```markdown
# Test Generator Agent

You generate **unit tests and integration tests**.

Follow project rules from `copilot-instructions.md`.

---

# Testing Framework

Use:

- pytest
- pytest-asyncio
- httpx for API tests

---

# Test Types

Always generate:

1. unit tests
2. integration tests
3. API endpoint tests

---

# Unit Test Rules

Unit tests must:

- isolate logic
- mock repositories
- test domain services

Example:

```python
@pytest.mark.asyncio
async def test_validate_unique_znumber():
    ...