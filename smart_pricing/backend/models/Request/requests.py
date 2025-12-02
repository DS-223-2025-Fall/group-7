# backend/models/requests/requests.py
from pydantic import BaseModel, Field, EmailStr
from decimal import Decimal

# =========================
# USER REQUEST MODELS
# =========================

class UserRegisterRequest(BaseModel):
    """
    Payload to register a new user.
    """
    email: EmailStr
    password: str = Field(min_length=6, description="Plain-text password (min 6 chars)")

class UserLoginRequest(BaseModel):
    """
    Payload to login an existing user.
    """
    email: EmailStr
    password: str

# =========================
# PROJECT REQUEST MODELS
# =========================

class CreateProjectRequestModel(BaseModel):
    """
    Create a pricing project. number_bandits is metadata; bandits are added separately.
    """
    description: str
    number_bandits: int = Field(..., ge=1)

class UpdateProjectRequestModel(BaseModel):
    """
    Update project fields.
    """
    description: str
    number_bandits: int = Field(..., ge=1)

# =========================
# BANDIT REQUEST MODELS
# =========================

class CreateBanditRequestModel(BaseModel):
    """
    Create a bandit (a price option) under a specific project.
    """
    price: Decimal

class UpdateBanditRequestModel(BaseModel):
    """
    Update bandit price.
    """
    price: Decimal

# =========================
# THOMPSON REQUEST MODELS
# =========================

class SubmitRewardRequest(BaseModel):
    """
    Submit a reward (float) for a bandit. decision is optional label describing the outcome.
    """
    reward: float
    decision: str | None = None

class RunSimulationRequest(BaseModel):
    """
    Run N simulated Thompson trials for a project.
    """
    n_trials: int = Field(..., ge=1)
