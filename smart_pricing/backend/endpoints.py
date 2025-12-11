from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime
import numpy as np
from fastapi import UploadFile, File
import os

from database.database import get_db
from database.models import Project, Bandit, Experiment
from database.schema import ExperimentCreate, BanditCreate

from models.Request.requests import (
    CreateProjectRequest,
    SubmitRewardRequest,
    CreateBanditRequestModel
)

from models.Response.responses import (
    ProjectResponse,
    BanditResponse,
    ExperimentResponse,
    ThompsonSelectResponse
)


router = APIRouter()

# ======================================================
#  CREATE PROJECT
# ======================================================
@router.post("/projects")
def create_project(request: CreateProjectRequest, db: Session = Depends(get_db)):

    project = Project(
        description=request.description,
        number_bandits=request.number_bandits,
        created_at=datetime.utcnow(),
        optimal_price=None,
        last_algorithm_run=None
    )
    db.add(project)
    db.commit()
    db.refresh(project)

    # 1 initial bandit
    bandit = Bandit(
        project_id=project.project_id,
        price=request.price,
        tau=1.0,
        lambd=1.0,
        mean=0.0,
        sum_rewards=0.0
    )
    db.add(bandit)
    db.commit()
    db.refresh(bandit)

    return {"project_id": project.project_id, "bandit_id": bandit.bandit_id}



@router.post("/projects/{project_id}/upload-image")
def upload_project_image(project_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):

    project = db.query(Project).filter_by(project_id=project_id).first()
    if not project:
        raise HTTPException(404, "Project not found")


    images_folder = "/backend/images"
    os.makedirs(images_folder, exist_ok=True)


    extension = file.filename.split(".")[-1]
    filename = f"project_{project_id}.{extension}"
    file_path = f"{images_folder}/{filename}"


    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())


    project.image_path = f"/images/{filename}"
    db.commit()

    return {"message": "Image uploaded", "image_path": project.image_path}



# ======================================================
#  GET PROJECTS
# ======================================================
@router.get("/projects")
def list_projects(db: Session = Depends(get_db)):
    return db.query(Project).order_by(Project.created_at.desc()).all()

# ======================================================
#  CREATE BANDIT
# ======================================================
@router.post("/projects/{project_id}/bandits")
def create_bandit(project_id: int, req: CreateBanditRequestModel, db: Session = Depends(get_db)):

    bandit = Bandit(
        project_id=project_id,
        price=req.price,
        tau=1.0,
        lambd=1.0,
        mean=0.0,
        sum_rewards=0.0
    )
    db.add(bandit)
    db.commit()
    db.refresh(bandit)

    return {
        "bandit_id": bandit.bandit_id,
        "project_id": project_id,
        "price": float(bandit.price)
    }

# ======================================================
#  THOMPSON SAMPLING SELECT (POST)
# ======================================================
@router.post("/projects/{project_id}/thompson/select", response_model=ThompsonSelectResponse)
def thompson_select_price(project_id: int, db: Session = Depends(get_db)):

    project = db.query(Project).filter_by(project_id=project_id).first()
    if not project:
        raise HTTPException(404, "Project not found")

    bandits = db.query(Bandit).filter_by(project_id=project_id).all()
    if not bandits:
        raise HTTPException(404, "No bandits found")

    samples = []
    for b in bandits:
        variance = 1.0 / b.lambd
        sample = np.random.normal(b.mean, np.sqrt(variance))
        samples.append((b.bandit_id, sample, b.price))

    bandit_id, sample, price = max(samples, key=lambda x: x[1])

    project.last_algorithm_run = datetime.utcnow()
    project.optimal_price = price
    db.commit()

    return {"bandit_id": bandit_id, "price": price}

# ======================================================
#  UPDATE REWARD
# ======================================================
@router.post("/bandits/{bandit_id}/thompson/reward")
def submit_reward(bandit_id: int, req: SubmitRewardRequest, db: Session = Depends(get_db)):

    bandit = db.query(Bandit).filter_by(bandit_id=bandit_id).first()
    if not bandit:
        raise HTTPException(404, "Bandit not found")

    project = db.query(Project).filter_by(project_id=bandit.project_id).first()

    # Save experiment
    experiment = Experiment(
        project_id=bandit.project_id,
        bandit_id=bandit_id,
        reward=req.reward,
        timestamp=datetime.utcnow(),
        decision=req.decision
    )
    db.add(experiment)

    # Bayesian update
    bandit.sum_rewards += req.reward
    bandit.lambd += bandit.tau
    bandit.mean = bandit.sum_rewards / bandit.lambd

    project.last_algorithm_run = datetime.utcnow()
    db.commit()

    return {"message": "Reward updated", "bandit_id": bandit_id, "new_mean": bandit.mean}
