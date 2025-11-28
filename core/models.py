"""
SQLAlchemy models for the project.

Defines the database tables for users, projects, bandits, and experiments.
Each model includes timestamps using Yerevan time.
"""

from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from pytz import timezone

Base = declarative_base()

def get_yerevan_time():
    """
    Returns the current time in the Asia/Yerevan timezone.
    """
    yerevan_tz = timezone("Asia/Yerevan")
    return datetime.now(yerevan_tz)

class User(Base):
    """
    User account stored in the system.

    Attributes:
        user_id: Primary key.
        email: User's email address.
        password_hash: Hashed password.
        created_at: Timestamp of account creation.
    """
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=get_yerevan_time)

class Project(Base):
    """
    Project entry containing bandit configurations and experiment history.

    Attributes:
        project_id: Primary key.
        description: Short project description.
        number_bandits: Number of bandits used in the project.
        created_at: Creation timestamp.
        optimal_price: Last computed optimal price.
        last_algorithm_run: Timestamp of the last algorithm execution.
        bandits: Related bandit arms.
        experiments: Related experiment records.
    """
    __tablename__ = "projects"

    project_id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(Text, nullable=False)
    number_bandits = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), default=get_yerevan_time)
    optimal_price = Column(Numeric, nullable=True)
    last_algorithm_run = Column(DateTime(timezone=True), nullable=True)

    bandits = relationship("Bandit", back_populates="project", cascade="all, delete-orphan")
    experiments = relationship("Experiment", back_populates="project", cascade="all, delete-orphan")

class Bandit(Base):
    """
    Bandit arm used in a project's pricing algorithm.

    Attributes:
        bandit_id: Primary key.
        project_id: Reference to the linked project.
        price: Price value for this bandit.
        mean: Mean estimate for rewards.
        variance: Variance estimate for rewards.
        reward: Most recent reward.
        trial: Number of times this bandit has been selected.
        number_explored: Number of exploration steps.
        updated_at: Timestamp of the last update.
        project: Parent project.
        experiments: Experiment records for this bandit.
    """
    __tablename__ = "bandits"

    bandit_id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.project_id"), nullable=False)
    price = Column(Numeric, nullable=False)
    mean = Column(Numeric, nullable=False, default=0.0)
    variance = Column(Numeric, nullable=False, default=1.0)
    reward = Column(Numeric, nullable=False, default=0.0)
    trial = Column(Integer, nullable=False, default=0)
    number_explored = Column(Integer, nullable=False, default=0)
    updated_at = Column(DateTime(timezone=True), default=get_yerevan_time)

    project = relationship("Project", back_populates="bandits")
    experiments = relationship("Experiment", back_populates="bandit", cascade="all, delete-orphan")

class Experiment(Base):
    """
    Experiment record linking a project, a bandit, and the result of a decision.

    Attributes:
        experiment_id: Primary key.
        project_id: Linked project.
        bandit_id: Bandit used in the experiment.
        decision: Action taken.
        reward: Reward received.
        start_date: Timestamp when the experiment started.
        end_date: Timestamp when the experiment ended.
    """
    __tablename__ = "experiments"

    experiment_id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.project_id"), nullable=False)
    bandit_id = Column(Integer, ForeignKey("bandits.bandit_id"), nullable=False)
    decision = Column(String, nullable=False)
    reward = Column(Numeric, nullable=False)
    start_date = Column(DateTime(timezone=True), default=get_yerevan_time)
    end_date = Column(DateTime(timezone=True), default=get_yerevan_time)

    project = relationship("Project", back_populates="experiments")
    bandit = relationship("Bandit", back_populates="experiments")
