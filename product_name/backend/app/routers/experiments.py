from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas import ExperimentRead
from app.services.experiments import ExperimentService

router = APIRouter(prefix="/experiments", tags=["Experiments"])


@router.get("", response_model=list[ExperimentRead])
async def list_experiments(db: AsyncSession = Depends(get_db)):
    return await ExperimentService.get_all_experiments(db)
