from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class ProjectCreate(BaseModel):
    description: str
    number_bandits: int
    prices: List[float]

class ProjectOut(BaseModel):
    project_id: int
    description: str
    number_bandits: int
    created_at: datetime

    class Config:
        from_attributes = True


class BanditOut(BaseModel):
    bandit_id: int
    price: float
    mean: float
    variance: float
    trial: int

    class Config:
        from_attributes = True


class ExperimentCreate(BaseModel):
    project_id: int
    bandit_id: int

class ExperimentOut(BaseModel):
    experiment_id: int
    project_id: int
    bandit_id: int
    reward: float
    decision: str
    start_date: datetime
    end_date: datetime

    class Config:
        from_attributes = True
