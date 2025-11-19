from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas import BanditCreate, BanditRead
from app.services.bandits import BanditService

router = APIRouter(prefix="/bandits", tags=["Bandits"])


@router.post("/{project_id}", response_model=BanditRead)
async def create_bandit(project_id: int, data: BanditCreate, db: AsyncSession = Depends(get_db)):
    return await BanditService.create_bandit(db, project_id, data.price)


@router.get("/{project_id}", response_model=list[BanditRead])
async def list_bandits(project_id: int, db: AsyncSession = Depends(get_db)):
    return await BanditService.get_bandits_by_project(db, project_id)
