from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies.db import get_async_db
from app.application.dtos.process import DonorProcessDetailsDTO
from app.application.use_cases.process import GetProcessByDonorUseCase
from app.infrastructure.db.repositories.process_repository import ProcessRepositoryORM

router = APIRouter()


@router.get("/processes-by-donor/{donor_id}", response_model=DonorProcessDetailsDTO)
async def get_processes_by_donor(donor_id: int, db=Depends(get_async_db)):
    repo = ProcessRepositoryORM(db)
    use_case = GetProcessByDonorUseCase(repo)

    result = await use_case.execute(donor_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Donor with ID {donor_id} not found",
        )

    return result
