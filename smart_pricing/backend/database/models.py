# backend/database/models.py

from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    ForeignKey,
    DateTime,
    Text
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


# -----------------------------
#  FIXED: Always return naive datetime
# -----------------------------
def get_naive_time():
    return datetime.utcnow()   # no timezone attached


# -----------------------------
#  USER MODEL
# -----------------------------
class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)

    created_at = Column(
        DateTime(timezone=False),
        default=get_naive_time,
        nullable=False
    )

    # Password methods optional — keep if needed
    def set_password(self, password: str):
        from passlib.context import CryptContext
        context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.password_hash = context.hash(password)

    def verify_password(self, password: str) -> bool:
        from passlib.context import CryptContext
        context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return context.verify(password, self.password_hash)


# -----------------------------
#  PROJECT MODEL
# -----------------------------
class Project(Base):
    __tablename__ = "projects"

    project_id = Column(Integer, primary_key=True, autoincrement=True)

    description = Column(Text, nullable=False)
    image_path = Column(String, nullable=True)
    number_bandits = Column(Integer, nullable=False)

    created_at = Column(
        DateTime(timezone=False),
        default=get_naive_time,
        nullable=False
    )

    optimal_price = Column(Numeric, nullable=True)
    last_algorithm_run = Column(DateTime(timezone=False), nullable=True)

    bandits = relationship("Bandit", back_populates="project", cascade="all, delete-orphan")
    experiments = relationship("Experiment", back_populates="project", cascade="all, delete-orphan")


# -----------------------------
#  BANDIT MODEL
# -----------------------------
class Bandit(Base):
    __tablename__ = "bandits"

    bandit_id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.project_id"), nullable=False)

    price = Column(Numeric, nullable=False)

    # Thompson sampling statistics
    mean = Column(Numeric, nullable=False, default=0.0)
    variance = Column(Numeric, nullable=False, default=1.0)
    reward = Column(Numeric, nullable=False, default=0.0)
    trial = Column(Integer, nullable=False, default=0)
    number_explored = Column(Integer, nullable=False, default=0)

    updated_at = Column(
        DateTime(timezone=False),
        default=get_naive_time,
        onupdate=get_naive_time
    )

    project = relationship("Project", back_populates="bandits")
    experiments = relationship("Experiment", back_populates="bandit", cascade="all, delete-orphan")


# -----------------------------
#  EXPERIMENT MODEL
# -----------------------------
class Experiment(Base):
    __tablename__ = "experiments"

    experiment_id = Column(Integer, primary_key=True, autoincrement=True)

    project_id = Column(Integer, ForeignKey("projects.project_id"), nullable=False)
    bandit_id = Column(Integer, ForeignKey("bandits.bandit_id"), nullable=False)

    decision = Column(String, nullable=False)
    reward = Column(Numeric, nullable=False)

    start_date = Column(DateTime(timezone=False), default=get_naive_time)
    end_date = Column(DateTime(timezone=False), default=get_naive_time)

    project = relationship("Project", back_populates="experiments")
    bandit = relationship("Bandit", back_populates="experiments")