from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ProjectCreate(BaseModel):
    description: str
    number_bandits: int


class ProjectRead(BaseModel):
    project_id: int
    description: str
    number_bandits: int
    created_at: datetime

    class Config:
        from_attributes = True


class BanditCreate(BaseModel):
    price: float


class BanditRead(BaseModel):
    bandit_id: int
    project_id: int
    price: float
    mean: float
    variance: float
    reward: float
    trial: int
    number_explored: int
    updated_at: datetime

    class Config:
        from_attributes = True


class ExperimentRead(BaseModel):
    experiment_id: int
    project_id: int
    bandit_id: int
    decision: Optional[str]
    reward: float
    start_date: datetime
    end_date: datetime

    class Config:
        from_attributes = True
