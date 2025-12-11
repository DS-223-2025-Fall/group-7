from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal


# =========================
# PROJECT RESPONSE MODELS
# =========================

class CreateProjectResponseModel(BaseModel):
    """
    Response model returned after creating a new project.

    Attributes:
        project_id (int): Unique identifier of the created project.
        description (str): Text description of the project.
        number_bandits (int): Number of price options (bandits) defined for the project.
        created_at (datetime): Timestamp of project creation.
        image_path (str | None): Optional file path to the project image.
    """
    project_id: int
    description: str
    number_bandits: int
    created_at: datetime
    image_path: str | None = None

    class Config:
        from_attributes = True


class ProjectItem(BaseModel):
    """
    A lightweight project item used when listing or retrieving multiple projects.

    Attributes:
        project_id (int): Unique project ID.
        description (str): Description of the project.
        number_bandits (int): Number of price options associated with the project.
        created_at (datetime): When this project was created.
        image_path (str | None): Optional associated image.
    """
    project_id: int
    description: str
    number_bandits: int
    created_at: datetime
    image_path: str | None = None

    class Config:
        from_attributes = True


class ProjectReport(BaseModel):
    """
    Detailed project report, including statistical analysis results.

    Attributes:
        project_id (int): Unique identifier of the project.
        description (str): Description of the project.
        number_bandits (int): Number of bandits (price points).
        created_at (datetime): Timestamp of creation.
        optimal_price (Decimal | None): Computed optimal price, if available.
        image_path (str | None): Path to the project's representative image.
    """
    project_id: int
    description: str
    number_bandits: int
    created_at: datetime
    optimal_price: Decimal | None = None
    image_path: str | None = None

    class Config:
        from_attributes = True


# =========================
# BANDIT RESPONSE MODELS
# =========================

class CreateBanditResponseModel(BaseModel):
    """
    Response model returned after creating a new bandit (price option).

    Attributes:
        bandit_id (int): Unique identifier of the created bandit.
        project_id (int): ID of the project this bandit belongs to.
        price (Decimal): Price value assigned to this bandit.
    """
    bandit_id: int
    project_id: int
    price: Decimal

    class Config:
        from_attributes = True


class BanditReport(BaseModel):
    """
    Detailed statistical report for a single bandit, including performance metrics.

    Attributes:
        bandit_id (int): Identifier of the bandit.
        project_id (int): ID of the related project.
        price (Decimal): Price level for this bandit.
        mean (Decimal): Estimated mean reward.
        variance (Decimal): Variance of the reward distribution.
        reward (Decimal): Total reward accumulated.
        trial (int): Number of trials observed.
        updated_at (datetime): Last update timestamp.
    """
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
    """
    Response returned after performing a Thompson Sampling selection step.

    Attributes:
        bandit_id (int): ID of the bandit selected by the algorithm.
        price (Decimal): Price associated with the selected bandit.
        reason (str | None): Optional explanation of why this bandit was chosen.
    """
    bandit_id: int
    price: Decimal
    reason: str | None = None

    class Config:
        from_attributes = True
