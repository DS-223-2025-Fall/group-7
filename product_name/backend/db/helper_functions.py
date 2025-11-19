from . import models
from .database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



def get_projects(db):
    return db.query(models.Project).all()

def get_project(db, project_id: int):
    return db.query(models.Project).filter(models.Project.project_id == project_id).first()

def create_project(db, description: str, number_bandits: int):
    project = models.Project(description=description, number_bandits=number_bandits)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def get_bandits_by_project(db, project_id: int):
    return db.query(models.Bandit).filter(models.Bandit.project_id == project_id).all()

def create_bandit(db, project_id: int, price: float):
    bandit = models.Bandit(project_id=project_id, price=price)
    db.add(bandit)
    db.commit()
    db.refresh(bandit)
    return bandit


def create_experiment(db, project_id: int, bandit_id: int, decision: str, reward: float):
    experiment = models.Experiment(
        project_id=project_id,
        bandit_id=bandit_id,
        decision=decision,
        reward=reward
    )
    db.add(experiment)
    db.commit()
    db.refresh(experiment)
    return experiment
