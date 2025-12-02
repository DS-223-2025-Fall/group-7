# backend/models/responses/responses.py
"""
Response schemas returned by the API.

These Pydantic models define the exact shape of JSON responses
that the backend sends to clients. They map directly from
SQLAlchemy ORM objects using `orm_mode = True`.
"""

from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal

# =========================
# USER RESPONSE MODELS
# =========================

class UserResponse(BaseModel):
    """Response returned after user registration or login."""
    user_id: int
    email: str
    created_at: datetime

    class Config:
        orm_mode = True

# =========================
# PROJECT RESPONSE MODELS
# =========================

class CreateProjectResponseModel(BaseModel):
    """Response returned when a new Project is created."""
    project_id: int
    description: str
    number_bandits: int
    created_at: datetime

    class Config:
        orm_mode = True

class ProjectItem(BaseModel):
    """Single item returned in the list of projects."""
    project_id: int
    description: str
    number_bandits: int
    created_at: datetime

    class Config:
        orm_mode = True

class ProjectReport(BaseModel):
    """Detailed project report with additional metadata."""
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
    """Response returned when a new Bandit is created."""
    bandit_id: int
    project_id: int
    price: Decimal

    class Config:
        orm_mode = True

class BanditReport(BaseModel):
    """Detailed bandit report, showing Gaussian posterior stats."""
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
    """
    Response returned when Thompson Sampling chooses
    a bandit for the next price test.
    """
    bandit_id: int
    price: Decimal
    reason: str | None = None

    class Config:
        orm_mode = True
