from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import get_db, engine
from models import Base
import crud
import schemas

# DO NOT enable until DB container is running
# Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/project/create")
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    return crud.create_project(db, project.description, project.prices)


@app.post("/project/{project_id}/pull")
def pull_arm(project_id: int, db: Session = Depends(get_db)):
    bandit, reward = crud.pull_bandit(db, project_id)
    return {
        "bandit_id": bandit.bandit_id,
        "price": bandit.price,
        "reward": reward,
        "mean": bandit.mean,
        "variance": bandit.variance,
        "trial": bandit.trial
    }


@app.get("/project/{project_id}/distributions")
def get_distributions(project_id: int, db: Session = Depends(get_db)):
    bandits = crud.get_distributions(db, project_id)
    return [
        {
            "bandit_id": b.bandit_id,
            "price": b.price,
            "mean": b.mean,
            "variance": b.variance,
            "trial": b.trial
        }
        for b in bandits
    ]
