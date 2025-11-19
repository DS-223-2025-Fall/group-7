from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from db import get_db, engine
from models import Base
from schemas import ProjectCreate, RewardUpdate
import crud


#Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/project/create")
def create_project(data: ProjectCreate, db: Session = Depends(get_db)):
    return crud.create_project(db, data.description, data.prices)


@app.get("/project/{project_id}/pull")
def pull_bandit(project_id: int, db: Session = Depends(get_db)):
    bandit = crud.pull_bandit(db, project_id)
    return {"bandit_id": bandit.bandit_id, "price": bandit.price}


@app.post("/bandit/{bandit_id}/reward")
def update_bandit(bandit_id: int, data: RewardUpdate, db: Session = Depends(get_db)):
    b = crud.update_bandit(db, bandit_id, data.reward)
    return {"status": "updated", "bandit_id": b.bandit_id, "new_mean": b.mean}


@app.get("/project/{project_id}/distributions")
def get_distributions(project_id: int, db: Session = Depends(get_db)):
    return crud.get_distributions(db, project_id)
