from fastapi import APIRouter

from app.api.v1.routers import donors

router = APIRouter()
router.include_router(donors.router, prefix="/v1", tags=["donors"])
