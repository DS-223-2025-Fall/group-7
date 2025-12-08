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
        from_attributes = True


# =========================
# PROJECT RESPONSE MODELS
# =========================

class CreateProjectResponseModel(BaseModel):
    project_id: int
    description: str
    number_bandits: int
    created_at: datetime
    image_path: str | None = None   # ✅ NEW

    class Config:
        from_attributes = True


class ProjectItem(BaseModel):
    project_id: int
    description: str
    number_bandits: int
    created_at: datetime
    image_path: str | None = None   # ✅ NEW

    class Config:
        from_attributes = True


class ProjectReport(BaseModel):
    project_id: int
    description: str
    number_bandits: int
    created_at: datetime
    optimal_price: Decimal | None = None
    image_path: str | None = None   # ✅ NEW

    class Config:
        from_attributes = True


# =========================
# BANDIT RESPONSE MODELS
# =========================

class CreateBanditResponseModel(BaseModel):
    bandit_id: int
    project_id: int
    price: Decimal

    class Config:
        from_attributes = True


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
        from_attributes = True


# =========================
# THOMPSON RESPONSE MODELS
# =========================

class ThompsonSelectResponse(BaseModel):
    bandit_id: int
    price: Decimal
    reason: str | None = None

    class Config:
        from_attributes = True