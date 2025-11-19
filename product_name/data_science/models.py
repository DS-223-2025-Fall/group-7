from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()


class Project(Base):
    __tablename__ = "projects"

    project_id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(255), nullable=False)
    number_bandits = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    bandits = relationship("Bandit", back_populates="project")
    experiments = relationship("Experiment", back_populates="project")


class Bandit(Base):
    __tablename__ = "bandits"

    bandit_id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.project_id"))
    price = Column(Float, nullable=False)

    mean = Column(Float, default=0.0)
    precision = Column(Float, default=1.0)
    tau = Column(Float, default=1.0)        
    sum_x = Column(Float, default=0.0)
    trial = Column(Integer, default=0)

    updated_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("Project", back_populates="bandits")
    experiments = relationship("Experiment", back_populates="bandit")


class Experiment(Base):
    __tablename__ = "experiments"

    experiment_id = Column(Integer, primary_key=True, autoincrement=True)
    
    project_id = Column(Integer, ForeignKey("projects.project_id"))
    bandit_id = Column(Integer, ForeignKey("bandits.bandit_id"))

    decision = Column(String(50))         
    reward = Column(Float)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, default=datetime.utcnow)

    project = relationship("Project", back_populates="experiments")
    bandit = relationship("Bandit", back_populates="experiments")
