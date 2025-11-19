import numpy as np
from sqlalchemy.orm import Session
from models import Bandit, Experiment
from datetime import datetime


def init_prior(bandit: Bandit):
    bandit.mean = 0.0
    bandit.precision = 1.0  
    bandit.tau = 1.0    
    bandit.sum_x = 0.0
    bandit.trial = 0
    return bandit


def sample_posterior(bandit: Bandit):
    std = np.sqrt(1.0 / bandit.precision)
    return np.random.randn() * std + bandit.mean


def choose_bandit(db: Session, project_id: int):
    bandits = db.query(Bandit).filter(Bandit.project_id == project_id).all()

    samples = [sample_posterior(b) for b in bandits]
    best_index = int(np.argmax(samples))
    return bandits[best_index]


def update_posterior(db: Session, bandit_id: int, reward: float):
    bandit = db.query(Bandit).filter(Bandit.bandit_id == bandit_id).first()

    bandit.precision += bandit.tau         
    bandit.sum_x += reward
    bandit.mean = (bandit.tau * bandit.sum_x) / bandit.precision
    bandit.trial += 1
    bandit.updated_at = datetime.utcnow()

    exp = Experiment(
        project_id=bandit.project_id,
        bandit_id=bandit.bandit_id,
        decision=str(bandit.price),
        reward=reward,
        start_date=datetime.utcnow(),
        end_date=datetime.utcnow(),
    )
    db.add(exp)

    db.commit()
    db.refresh(bandit)
    return bandit
