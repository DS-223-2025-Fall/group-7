from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.database import engine, Base
from app.routers import projects, bandits, experiments


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

app = FastAPI(
    title="Smart Pricing API",
    lifespan=lifespan
)

app.include_router(projects.router)
app.include_router(bandits.router)
app.include_router(experiments.router)

@app.get("/")
async def root():
    return {"message": "FastAPI backend is running!"}

