from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies.db import get_async_db
from app.api.schemas.donor import DonorCreate, DonorResponse, DonorListResponse
from app.application.dtos.donor import (
    CreateDonorInputDTO,
    DonorOutputDTO,
    DonorListDTO,
)
from app.application.use_cases.donor import AddDonorUseCase, ListDonorsUseCase
from app.container.di_container import DIContainer
from app.infrastructure.db.repositories.donor_repository import DonorRepositoryORM

router = APIRouter()


@router.post("/donors", response_model=DonorResponse, status_code=status.HTTP_201_CREATED)
async def create_donor(payload: DonorCreate, db=Depends(get_async_db)):
    """Create a new donor.
    
    Data flow:
    1. Validate incoming request with DonorCreate schema (Pydantic)
    2. Convert schema to input DTO (CreateDonorInputDTO - dataclass)
    3. Pass input DTO to use case
    4. Use case returns domain entity
    5. Convert domain entity to output DTO (DonorOutputDTO - dataclass)
    6. Convert output DTO to response schema (DonorResponse - Pydantic) for serialization
    """
    # Convert schema to input DTO (API layer → Application layer)
    #input_dto = CreateDonorInputDTO.from_schema(payload)  # type: ignore 
    input_dto = CreateDonorInputDTO(**payload.model_dump())  
    
    # Create repository and use case
    repo = DonorRepositoryORM(db)
    use_case = AddDonorUseCase(repo)
    
    # Execute use case, which returns domain entity
    domain_donor = await use_case.execute(input_dto)
    
    # Convert domain entity to output DTO (Domain layer → Application layer)
    #output_dto = DonorOutputDTO.from_domain(domain_donor)# type: ignore
    output_dto = DonorOutputDTO(**vars(domain_donor))  
    
    # Convert output DTO to response schema for serialization and return
    return DonorResponse.model_validate(output_dto, from_attributes=True)


@router.get("/donors", response_model=DonorListResponse)
async def list_donors(
    znumber: int | None = None,
    region: str | None = None,
    search: str | None = None,
    order_by: str | None = None,
    order_dir: str = "asc",
    page: int = 1,
    per_page: int = 20,
    db=Depends(get_async_db),
):
    """List donors with filtering, search, sorting, and pagination.
    
    Data flow:
    1. Build filters from query parameters
    2. Pass filters to use case
    3. Use case returns domain entities and total count
    4. Convert each domain entity to output DTO
    5. Convert output DTOs to response schema for serialization
    """
    # Build filters from query parameters
    filters = {}
    if znumber is not None:
        filters["znumber"] = znumber
    if region is not None:
        filters["region"] = region

    # Create repository and use case
    repo = DonorRepositoryORM(db)
    use_case = ListDonorsUseCase(repo)
    
    # Execute use case, which returns domain entities and count
    items, total = await use_case.execute(
        filters=filters,
        search=search,
        order_by=order_by,
        order_dir=order_dir,
        page=page,
        per_page=per_page,
    )
    
    # Convert domain entities to output DTOs (Domain layer → Application layer)
    output_dtos = [DonorOutputDTO.from_domain(item) for item in items]
    
    # Create list DTO
    list_dto = DonorListDTO(
        items=output_dtos,
        total=total,
        page=page,
        per_page=per_page,
    )
    
    # Convert to response schema for serialization and return
    return DonorListResponse.model_validate(list_dto, from_attributes=True)
