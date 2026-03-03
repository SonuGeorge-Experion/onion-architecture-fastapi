from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies.db import get_async_db
from app.api.schemas.donor import DonorCreate
from app.application.dtos.donor import DonorDTO, DonorListDTO
from app.application.use_cases.donor import AddDonorUseCase, ListDonorsUseCase
from app.container.di_container import DIContainer
from app.infrastructure.db.repositories.donor_repository import DonorRepositoryORM

router = APIRouter()


@router.post("/donors", response_model=DonorDTO, status_code=status.HTTP_201_CREATED)
async def create_donor(payload: DonorCreate, db=Depends(get_async_db)):
    repo = DonorRepositoryORM(db)
    use_case = AddDonorUseCase(repo)
    donor = await use_case.execute(payload.model_dump())
    return donor


@router.get("/donors", response_model=DonorListDTO)
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
    repo = DonorRepositoryORM(db)
    use_case = ListDonorsUseCase(repo)
    filters = {}
    if znumber is not None:
        filters["znumber"] = znumber
    if region is not None:
        filters["region"] = region

    result = await use_case.execute(
        filters=filters,
        search=search,
        order_by=order_by,
        order_dir=order_dir,
        page=page,
        per_page=per_page,
    )
    return result
