from sqlalchemy.orm import Session
from datetime import datetime

from models import Project, Bandit, Experiment
from bandits.gaussian_ts import (
    init_prior,
    choose_bandit,
    update_posterior,
)

def create_project(db: Session, description: str, prices: list[int]):
    project = Project(
        description=description,
        number_bandits=len(prices),
        created_at=datetime.utcnow()
    )
    db.add(project)
    db.commit()
    db.refresh(project)

    for price in prices:
        bandit = Bandit(project_id=project.project_id, price=price)
        init_prior(bandit)
        db.add(bandit)

    db.commit()
    return project


def pull_bandit(db: Session, project_id: int):
    return choose_bandit(db, project_id)


def update_bandit(db: Session, bandit_id: int, reward: float):
    return update_posterior(db, bandit_id, reward)


def get_distributions(db: Session, project_id: int):
    bandits = db.query(Bandit).filter(Bandit.project_id == project_id).all()

    dist = []
    for b in bandits:
        dist.append({
            "bandit_id": b.bandit_id,
            "price": b.price,
            "mean": b.mean,
            "variance": 1.0 / b.precision,
            "trials": b.trial
        })
    return dist
