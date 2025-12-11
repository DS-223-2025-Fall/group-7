from pydantic import BaseModel, Field, EmailStr
from decimal import Decimal
from typing import Optional


# =========================
# PROJECT REQUEST MODELS
# =========================

class CreateProjectRequest(BaseModel):
    """
    Request model for creating a new project (product).

    This payload is sent when a user wants to initialize a new project in the system.
    It contains metadata describing the project and the number of bandits (price options)
    that will be generated when the project is created.

    Attributes:
        description (str): Textual description of the project.
        number_bandits (int): Number of price options (bandits) to create. Must be >= 1.
    """
    description: str
    number_bandits: int = Field(..., ge=1, description="Number of price options to be created")


class UpdateProjectRequestModel(BaseModel):
    """
    Request model for updating an existing project's metadata.

    Attributes:
        description (str): Updated project description.
        number_bandits (int): Updated number of bandits. Must remain >= 1.
    """
    description: str
    number_bandits: int = Field(..., ge=1)


# =========================
# BANDIT REQUEST MODELS
# =========================

class CreateBanditRequestModel(BaseModel):
    """
    Request model for creating a new bandit (price option).

    A bandit represents a specific price point in the Thompson Sampling model.

    Attributes:
        price (Decimal): The price assigned to this bandit.
    """
    price: Decimal = Field(..., description="Price assigned to this bandit")


class UpdateBanditRequestModel(BaseModel):
    """
    Request model for updating an existing bandit's price.

    Attributes:
        price (Decimal): The updated price value for the bandit.
    """
    price: Decimal


# =========================
# THOMPSON REQUEST MODELS
# =========================

class SubmitRewardRequest(BaseModel):
    """
    Request model for submitting a reward after a user interaction with a bandit.

    This updates the Thompson Sampling posterior by providing a reward signal.

    Attributes:
        reward (float): Numeric reward value (e.g., 1 = purchase, 0 = no purchase).
        decision (Optional[str]): Optional text describing the source or context of the event.
    """
    reward: float
    decision: Optional[str] = None


class RunSimulationRequest(BaseModel):
    """
    Request model for running multiple simulated Thompson Sampling trials.

    Attributes:
        n_trials (int): Number of simulation trials to execute. Must be >= 1.
    """
    n_trials: int = Field(..., ge=1, description="Number of simulation trials to run")
