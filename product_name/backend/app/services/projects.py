from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app import models

class ProjectService:

    @staticmethod
    async def create_project(db: AsyncSession, description: str, number_bandits: int):
        project = models.Project(
            description=description,
            number_bandits=number_bandits
        )
        db.add(project)
        await db.commit()
        await db.refresh(project)
        return project

    @staticmethod
    async def get_all_projects(db: AsyncSession):
        result = await db.execute(select(models.Project))
        return result.scalars().all()

    @staticmethod
    async def get_project(db: AsyncSession, project_id: int):
        result = await db.execute(
            select(models.Project).where(models.Project.project_id == project_id)
        )
        return result.scalar_one_or_none()
