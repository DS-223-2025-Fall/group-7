from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base

class Project(Base):
    __tablename__ = "projects"

    project_id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    number_bandits = Column(Integer, nullable=False)

    bandits = relationship("Bandit", back_populates="project")


class Bandit(Base):
    __tablename__ = "bandits"

    bandit_id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.project_id"))
    price = Column(Numeric, nullable=False)
    mean = Column(Numeric, default=0.0)
    variance = Column(Numeric, default=1.0)
    reward = Column(Numeric, default=0.0)
    trial = Column(Integer, default=0)
    number_explored = Column(Integer, default=0)
    updated_at = Column(TIMESTAMP, server_default=func.now())

    project = relationship("Project", back_populates="bandits")


class Experiment(Base):
    __tablename__ = "experiments"

    experiment_id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.project_id"))
    bandit_id = Column(Integer, ForeignKey("bandits.bandit_id"))
    decision = Column(String)
    reward = Column(Numeric, nullable=False)
    start_date = Column(TIMESTAMP, server_default=func.now())
    end_date = Column(TIMESTAMP, server_default=func.now())
