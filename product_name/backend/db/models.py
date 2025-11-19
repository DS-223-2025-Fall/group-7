from sqlalchemy import Column, Integer, String, Text, Numeric, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from pytz import timezone

Base = declarative_base()


def get_yerevan_time():
    """
    Returns the current time in the Yerevan timezone.
    """
    yerevan_tz = timezone('Asia/Yerevan')
    return datetime.now(yerevan_tz)


class Project(Base):
    """
    Represents a project in the smart pricing system.

    Attributes:
        project_id (int): Primary key.
        description (str): Description of the project.
        number_bandits (int): Number of bandits in this project.
        created_at (DateTime): Project creation timestamp.
    """
    __tablename__ = "projects"

    project_id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(Text, nullable=False)
    number_bandits = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=get_yerevan_time)


    bandits = relationship("Bandit", back_populates="project")
    experiments = relationship("Experiment", back_populates="project")


class Bandit(Base):
    """
    Represents a bandit in a project.

    Attributes:
        bandit_id (int): Primary key.
        project_id (int): Foreign key to Project.
        price (float): Price for this bandit option.
        mean (float): Mean reward estimate.
        variance (float): Variance of reward estimate.
        reward (float): Total reward observed.
        trial (int): Number of trials.
        number_explored (int): Count of explorations.
        updated_at (DateTime): Last update timestamp.
    """
    __tablename__ = "bandits"

    bandit_id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.project_id"))
    price = Column(Numeric, nullable=False)
    mean = Column(Numeric, default=0.0)
    variance = Column(Numeric, default=1.0)
    reward = Column(Numeric, default=0.0)
    trial = Column(Integer, default=0)
    number_explored = Column(Integer, default=0)
    updated_at = Column(DateTime, default=get_yerevan_time)


    project = relationship("Project", back_populates="bandits")
    experiments = relationship("Experiment", back_populates="bandit")


class Experiment(Base):
    """
    Represents an experiment (decision) in the smart pricing system.

    Attributes:
        experiment_id (int): Primary key.
        project_id (int): Foreign key to Project.
        bandit_id (int): Foreign key to Bandit.
        decision (str): Decision made (e.g., selected price).
        reward (float): Observed reward for this experiment.
        start_date (DateTime): Experiment start timestamp.
        end_date (DateTime): Experiment end timestamp.
    """
    __tablename__ = "experiments"

    experiment_id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.project_id"))
    bandit_id = Column(Integer, ForeignKey("bandits.bandit_id"))
    decision = Column(String)
    reward = Column(Numeric, nullable=False)
    start_date = Column(DateTime, default=get_yerevan_time)
    end_date = Column(DateTime, default=get_yerevan_time)


    project = relationship("Project", back_populates="experiments")
    bandit = relationship("Bandit", back_populates="experiments")
