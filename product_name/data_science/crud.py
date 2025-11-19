from sqlalchemy.orm import Session
from datetime import datetime
from models import Project, Bandit, Experiment
from bandits.gaussian_ts import sample_bandit, update_bandit_params


def create_project(db: Session, description: str, prices: list):
    project = Project(
        description=description,
        number_bandits=len(prices),
        created_at=datetime.utcnow()
    )
    db.add(project)
    db.commit()
    db.refresh(project)

    for p in prices:
        bandit = Bandit(
            project_id=project.project_id,
            price=p,
            mean=0.0,
            variance=1.0,
            reward=0,
            trial=0,
        )
        db.add(bandit)

    db.commit()
    return project


def select_bandit(db: Session, project_id: int):
    bandits = db.query(Bandit).filter(Bandit.project_id == project_id).all()
    if not bandits:
        return None

    samples = [sample_bandit(b.mean, b.variance) for b in bandits]
    best_idx = samples.index(max(samples))

    return bandits[best_idx]


def pull_bandit(db: Session, project_id: int):
    bandit = select_bandit(db, project_id)
    if not bandit:
        return None

    reward = sample_bandit(bandit.mean, bandit.variance)

    update_bandit_params(bandit, reward)

    bandit.reward = reward
    bandit.updated_at = datetime.utcnow()

    exp = Experiment(
        project_id=project_id,
        bandit_id=bandit.bandit_id,
        decision=str(bandit.price),
        reward=reward,
        start_date=datetime.utcnow(),
        end_date=datetime.utcnow()
    )
    db.add(exp)
    db.commit()

    return bandit, reward

def get_distributions(db: Session, project_id: int):
    bandits = db.query(Bandit).filter(Bandit.project_id == project_id).all()
    return bandits
