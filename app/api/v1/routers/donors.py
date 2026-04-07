import math

from fastapi import APIRouter, Depends, status

from app.api.dependencies.db import get_async_db
from app.api.schemas.donor import DonorCreate
from app.api.v1.responses import (
    ErrorResponse,
    PaginatedResponse,
    PaginationMeta,
    SuccessResponse,
)
from app.application.dtos.donor import (
    CreateDonorInputDTO,
    DonorOutputDTO,
)
from app.application.use_cases.donor import AddDonorUseCase, ListDonorsUseCase
from app.infrastructure.db.repositories.donor_repository import DonorRepositoryORM

router = APIRouter()


@router.post(
    "/donors",
    response_model=SuccessResponse[DonorOutputDTO],
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "description": "Donor created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "success": "true",
                        "message": "Donor created successfully",
                        "data": {
                            "donor_id": 8,
                            "znumber": 46371,
                            "name": "joe5",
                            "age": 63,
                            "region": "CA",
                            "other_factors": {"additionalProp1": {}},
                        },
                    }
                }
            },
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "description": "Bad Request",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorResponse,
            "description": "Validation Error",
            "content": {
                "application/json": {
                    "example": {
                        "success": False,
                        "error": {
                            "code": "VALIDATION_ERROR",
                            "type": "RequestValidationError",
                            "message": "Invalid request data",
                            "details": [
                                {
                                    "loc": ["body", "name"],
                                    "msg": "field required",
                                    "type": "value_error",
                                }
                            ],
                        },
                    }
                }
            },
        },
    },
)
async def create_donor(payload: DonorCreate, db=Depends(get_async_db)):
    """Create a new donor.

    Data flow:
    1. Validate incoming request with DonorCreate schema (Pydantic)
    2. Convert schema to input DTO (CreateDonorInputDTO - dataclass)
    3. Pass input DTO to use case
    4. Use case returns domain entity
    5. Convert domain entity to output DTO (DonorOutputDTO - dataclass)
    6. Convert output DTO to response schema (DonorResponse - Pydantic)
    for serialization
    7. Wrap in standard SuccessResponse
    """
    # Convert schema to input DTO (API layer → Application layer)
    # input_dto = CreateDonorInputDTO.from_schema(payload)  # type: ignore
    input_dto = CreateDonorInputDTO(**payload.model_dump())

    # Create repository and use case
    repo = DonorRepositoryORM(db)
    use_case = AddDonorUseCase(repo)

    # Execute use case, which returns domain entity
    domain_donor = await use_case.execute(input_dto)

    # Convert domain entity to output DTO (Domain layer → Application layer)
    # output_dto = DonorOutputDTO.from_domain(domain_donor)# type: ignore
    output_dto = DonorOutputDTO(**vars(domain_donor))

    # Convert output DTO to response schema for serialization
    # donor_response = DonorResponse.model_validate(output_dto, from_attributes=True)
    return SuccessResponse(message="Donor created successfully", data=output_dto)


@router.get(
    "/donors",
    response_model=PaginatedResponse[DonorOutputDTO],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "description": "Bad Request",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorResponse,
            "description": "Validation Error",
            "content": {
                "application/json": {
                    "example": {
                        "success": False,
                        "error": {
                            "code": "VALIDATION_ERROR",
                            "type": "RequestValidationError",
                            "message": "Invalid query parameters",
                            "details": [
                                {
                                    "loc": ["query", "page"],
                                    "msg": "value is not a valid integer",
                                    "type": "type_error.integer",
                                }
                            ],
                        },
                    }
                }
            },
        },
    },
)
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
    6. Wrap in standard PaginatedResponse
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

    # Create response objects
    # donor_responses = [
    #     DonorResponse.model_validate(dto, from_attributes=True) for dto in output_dtos
    # ]

    # Calculate pagination metadata
    total_pages = math.ceil(total / per_page) if per_page > 0 else 1

    # Return as PaginatedResponse
    return PaginatedResponse(
        message="Donors retrieved successfully",
        data=output_dtos,
        pagination=PaginationMeta(
            total=total, page=page, per_page=per_page, total_pages=total_pages
        ),
    )
