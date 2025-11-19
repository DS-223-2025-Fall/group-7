from pydantic import BaseModel

class ProjectCreate(BaseModel):
    description: str
    prices: list[int]


class RewardUpdate(BaseModel):
    reward: float
