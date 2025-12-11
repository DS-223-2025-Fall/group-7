from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal

# =========================
# USER RESPONSE MODELS
# =========================

class UserResponse(BaseModel):
    user_id: int
    email: str
    created_at: datetime

    class Config:
        orm_mode = True

# =========================
# PROJECT RESPONSE MODELS
# =========================

class CreateProjectResponseModel(BaseModel):
    project_id: int
    description: str
    number_bandits: int
    created_at: datetime

    class Config:
        orm_mode = True

class ProjectItem(BaseModel):
    project_id: int
    description: str
    number_bandits: int
    created_at: datetime

    class Config:
        orm_mode = True

class ProjectReport(BaseModel):
    project_id: int
    description: str
    number_bandits: int
    created_at: datetime
    optimal_price: Decimal | None = None

    class Config:
        orm_mode = True

# =========================
# BANDIT RESPONSE MODELS
# =========================

class CreateBanditResponseModel(BaseModel):
    bandit_id: int
    project_id: int
    price: Decimal

    class Config:
        orm_mode = True

class BanditReport(BaseModel):
    bandit_id: int
    project_id: int
    price: Decimal
    mean: Decimal
    variance: Decimal
    reward: Decimal
    trial: int
    updated_at: datetime

    class Config:
        orm_mode = True

# =========================
# THOMPSON RESPONSE MODELS
# =========================

class ThompsonSelectResponse(BaseModel):
    bandit_id: int
    price: Decimal
    reason: str | None = None

    class Config:
        orm_mode = True
