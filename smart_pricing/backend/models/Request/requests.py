from pydantic import BaseModel, Field, EmailStr
from decimal import Decimal

# =========================
# USER REQUEST MODELS
# =========================

class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

# =========================
# PROJECT REQUEST MODELS
# =========================

class CreateProjectRequest(BaseModel):
    description: str
    number_bandits: int = Field(..., ge=1)
    price: Decimal

class UpdateProjectRequestModel(BaseModel):
    description: str
    number_bandits: int = Field(..., ge=1)

# =========================
# BANDIT REQUEST MODELS
# =========================

class CreateBanditRequestModel(BaseModel):
    price: Decimal

class UpdateBanditRequestModel(BaseModel):
    price: Decimal

# =========================
# THOMPSON REQUEST MODELS
# =========================

class SubmitRewardRequest(BaseModel):
    reward: float
    decision: str | None = None

class RunSimulationRequest(BaseModel):
    n_trials: int = Field(..., ge=1)
