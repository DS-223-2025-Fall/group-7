# backend/database/models.py
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from pytz import timezone
from passlib.context import CryptContext

Base = declarative_base()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_yerevan_time():
    yerevan_tz = timezone("Asia/Yerevan")
    return datetime.now(yerevan_tz)

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=get_yerevan_time)

    def set_password(self, password: str):
        """Hash and set the user's password."""
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        """Verify a plain password against the stored hash."""
        return pwd_context.verify(password, self.password_hash)

class Project(Base):
    __tablename__ = "projects"

    project_id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(Text, nullable=False)
    image_path = Column(String, nullable=True)
    number_bandits = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), default=get_yerevan_time)
    optimal_price = Column(Numeric, nullable=True)
    last_algorithm_run = Column(DateTime(timezone=True), nullable=True)

    bandits = relationship("Bandit", back_populates="project", cascade="all, delete-orphan")
    experiments = relationship("Experiment", back_populates="project", cascade="all, delete-orphan")

class Bandit(Base):
    __tablename__ = "bandits"

    bandit_id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.project_id"), nullable=False)
    price = Column(Numeric, nullable=False)
    mean = Column(Numeric, nullable=False, default=0.0)
    variance = Column(Numeric, nullable=False, default=1.0)   # stores lambda (precision-like)
    reward = Column(Numeric, nullable=False, default=0.0)     # used as sum_x
    trial = Column(Integer, nullable=False, default=0)
    number_explored = Column(Integer, nullable=False, default=0)
    updated_at = Column(DateTime(timezone=True), default=get_yerevan_time)

    project = relationship("Project", back_populates="bandits")
    experiments = relationship("Experiment", back_populates="bandit", cascade="all, delete-orphan")

class Experiment(Base):
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
