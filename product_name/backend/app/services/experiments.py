from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app import models

class ExperimentService:

    @staticmethod
    async def get_all_experiments(db: AsyncSession):
        result = await db.execute(select(models.Experiment))
        return result.scalars().all()
