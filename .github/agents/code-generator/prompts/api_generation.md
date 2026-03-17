# API Generation Prompt

Generate FastAPI router code.

Rules:

- router must be thin
- business logic belongs to usecases
- use dependency injection
- return response schemas

Example pattern:

@router.post("/", response_model=DonorResponse)
async def create_donor(
    request: DonorCreateRequest,
    usecase: CreateDonorUseCase = Depends()
):
    return await usecase.execute(request)

Routers must not contain:

- SQLAlchemy2 queries
- domain logic