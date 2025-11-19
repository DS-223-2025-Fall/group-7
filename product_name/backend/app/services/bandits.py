from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app import models

class BanditService:

    @staticmethod
    async def create_bandit(db: AsyncSession, project_id: int, price: float):
        bandit = models.Bandit(
            project_id=project_id,
            price=price
        )
        db.add(bandit)
        await db.commit()
        await db.refresh(bandit)
        return bandit

    @staticmethod
    async def get_bandits_by_project(db: AsyncSession, project_id: int):
        result = await db.execute(
            select(models.Bandit).where(models.Bandit.project_id == project_id)
        )
        return result.scalars().all()
