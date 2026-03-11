from fastapi import APIRouter

from app.api.v1.routers import donors, process

router = APIRouter()
router.include_router(donors.router, prefix="/v1", tags=["donors"])
router.include_router(process.router, prefix="/v1", tags=["processes"])
