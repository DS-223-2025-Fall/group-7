# backend/endpoints.py
from fastapi import FastAPI, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from typing import List
from io import BytesIO

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from datetime import datetime

from database.database import get_db, create_tables
from database.models import User, Project, Bandit, Experiment
from database.schema import PROJECT_DESCRIPTION, TAGS_METADATA

from models import (
    UserRegisterRequest, UserLoginRequest,
    CreateProjectRequestModel, UpdateProjectRequestModel,
    CreateBanditRequestModel, UpdateBanditRequestModel,
    SubmitRewardRequest, RunSimulationRequest,
    UserResponse, CreateProjectResponseModel, ProjectItem, ProjectReport,
    CreateBanditResponseModel, BanditReport, ThompsonSelectResponse
)


# Algorithm hyperparameter (precision increment)
TAU = 1.0

app = FastAPI(
    title="Smart Pricing Backend Service",
    description=PROJECT_DESCRIPTION,
    openapi_tags=TAGS_METADATA
)

@app.on_event("startup")
def on_startup():
    """Create tables at startup (development convenience)."""
    create_tables()

# ------------------------
# HEALTH
# ------------------------
@app.get("/", tags=["Health"])
def root():
    """Health check endpoint."""
    return {"message": "Backend running"}

# ------------------------
# AUTH
# ------------------------
@app.post("/auth/register", response_model=UserResponse, tags=["Auth"])
def register_user(payload: UserRegisterRequest, db: Session = Depends(get_db)):
    """
    Register a new user.
    - Ensures email uniqueness
    - Stores hashed password
    """
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(email=payload.email)
    new_user.set_password(payload.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/auth/login", response_model=UserResponse, tags=["Auth"])
def login_user(payload: UserLoginRequest, db: Session = Depends(get_db)):
    """
    Login user (simple demo — returns user info; not issuing tokens here).
    """
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not user.verify_password(payload.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user

# ------------------------
# PROJECTS CRUD
# ------------------------
@app.post("/projects", response_model=CreateProjectResponseModel, tags=["Projects"])
def create_project(payload: CreateProjectRequestModel, db: Session = Depends(get_db)):
    """
    Create a new pricing project. Bandits are added separately.
    """
    project = Project(
        description=payload.description,
        number_bandits=payload.number_bandits
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

@app.get("/projects", response_model=List[ProjectItem], tags=["Projects"])
def list_projects(db: Session = Depends(get_db)):
    """List all projects."""
    return db.query(Project).all()

@app.get("/projects/{project_id}", response_model=ProjectReport, tags=["Projects"])
def get_project(project_id: int, db: Session = Depends(get_db)):
    """Get project by id."""
    project = db.query(Project).filter(Project.project_id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@app.put("/projects/{project_id}", response_model=ProjectReport, tags=["Projects"])
def update_project(project_id: int, payload: UpdateProjectRequestModel, db: Session = Depends(get_db)):
    """Update a project."""
    project = db.query(Project).filter(Project.project_id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    project.description = payload.description
    project.number_bandits = payload.number_bandits
    db.commit()
    db.refresh(project)
    return project

@app.delete("/projects/{project_id}", tags=["Projects"])
def delete_project(project_id: int, db: Session = Depends(get_db)):
    """Delete a project and its bandits/experiments."""
    project = db.query(Project).filter(Project.project_id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(project)
    db.commit()
    return {"message": "Project deleted"}

# ------------------------
# BANDITS CRUD
# ------------------------
@app.post("/projects/{project_id}/bandits", response_model=CreateBanditResponseModel, tags=["Bandits"])
def create_bandit(project_id: int, payload: CreateBanditRequestModel, db: Session = Depends(get_db)):
    """
    Create a bandit (price arm) for a project.
    """
    project = db.query(Project).filter(Project.project_id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    bandit = Bandit(
        project_id=project_id,
        price=payload.price,
        mean=0.0,
        variance=1.0,
        reward=0.0,
        trial=0
    )
    db.add(bandit)
    db.commit()
    db.refresh(bandit)
    return bandit

@app.get("/projects/{project_id}/bandits", response_model=List[BanditReport], tags=["Bandits"])
def list_bandits(project_id: int, db: Session = Depends(get_db)):
    """List bandits for a project."""
    return db.query(Bandit).filter(Bandit.project_id == project_id).all()

@app.get("/bandits/{bandit_id}", response_model=BanditReport, tags=["Bandits"])
def get_bandit(bandit_id: int, db: Session = Depends(get_db)):
    """Get a bandit by id."""
    b = db.query(Bandit).filter(Bandit.bandit_id == bandit_id).first()
    if not b:
        raise HTTPException(status_code=404, detail="Bandit not found")
    return b

@app.put("/bandits/{bandit_id}", response_model=BanditReport, tags=["Bandits"])
def update_bandit(bandit_id: int, payload: UpdateBanditRequestModel, db: Session = Depends(get_db)):
    """Update bandit properties."""
    b = db.query(Bandit).filter(Bandit.bandit_id == bandit_id).first()
    if not b:
        raise HTTPException(status_code=404, detail="Bandit not found")
    b.price = payload.price
    b.updated_at = datetime.now()
    db.commit()
    db.refresh(b)
    return b

@app.delete("/bandits/{bandit_id}", tags=["Bandits"])
def delete_bandit(bandit_id: int, db: Session = Depends(get_db)):
    """Delete a bandit."""
    b = db.query(Bandit).filter(Bandit.bandit_id == bandit_id).first()
    if not b:
        raise HTTPException(status_code=404, detail="Bandit not found")
    db.delete(b)
    db.commit()
    return {"message": "Bandit deleted"}

# ------------------------
# THOMPSON SAMPLING
# ------------------------
def _sample_bandit_draw(bandit: Bandit) -> float:
    """
    Draw sample from N(mean, std) where std = 1/sqrt(variance).
    `variance` column stores lambda-like precision; we interpret std = 1/sqrt(lambda).
    """
    mean = float(bandit.mean)
    lambda_ = float(bandit.variance)
    std = 1.0 / np.sqrt(lambda_) if lambda_ > 0 else 1.0
    return np.random.normal(mean, std)

@app.post("/projects/{project_id}/thompson/select", response_model=ThompsonSelectResponse, tags=["Thompson"])
def thompson_select(project_id: int, db: Session = Depends(get_db)):
    """
    Select a bandit using Gaussian Thompson Sampling:
    - For each bandit draw a sample ~ N(mean, 1/sqrt(variance))
    - Return bandit with highest sample
    """
    bandits = db.query(Bandit).filter(Bandit.project_id == project_id).all()
    if not bandits:
        raise HTTPException(status_code=404, detail="No bandits for this project")
    samples = [_sample_bandit_draw(b) for b in bandits]
    best_idx = int(np.argmax(samples))
    chosen = bandits[best_idx]
    return ThompsonSelectResponse(bandit_id=chosen.bandit_id, price=float(chosen.price), reason="Thompson sample chosen")

@app.post("/bandits/{bandit_id}/thompson/reward", tags=["Thompson"])
def thompson_submit_reward(bandit_id: int, payload: SubmitRewardRequest, db: Session = Depends(get_db)):
    """
    Submit a reward for a bandit and update Gaussian posterior.
    Posterior update used in your notebooks:
        lambda_new = lambda_old + TAU
        sum_x_new = sum_x_old + reward
        mean_new = (TAU * sum_x_new) / lambda_new
    """
    b = db.query(Bandit).filter(Bandit.bandit_id == bandit_id).first()
    if not b:
        raise HTTPException(status_code=404, detail="Bandit not found")

    reward = float(payload.reward)

    exp = Experiment(
        project_id=b.project_id,
        bandit_id=b.bandit_id,
        decision=payload.decision or "api",
        reward=reward,
        start_date=datetime.now(),
        end_date=datetime.now()
    )
    db.add(exp)

    lam_old = float(b.variance)
    sum_x_old = float(b.reward)

    lam_new = lam_old + TAU
    sum_x_new = sum_x_old + reward
    mean_new = (TAU * sum_x_new) / lam_new

    b.variance = lam_new
    b.reward = sum_x_new
    b.mean = mean_new
    b.trial = int(b.trial) + 1
    b.updated_at = datetime.now()

    db.commit()
    db.refresh(b)
    return {"message": "Reward submitted", "bandit_id": b.bandit_id, "new_mean": float(b.mean), "trials": b.trial}

@app.post("/projects/{project_id}/thompson/run", tags=["Thompson"])
def run_thompson_simulation(project_id: int, payload: RunSimulationRequest, db: Session = Depends(get_db)):
    """
    Run simulated Thompson Sampling using reward = price (deterministic reward) for n_trials.
    """
    bandits = db.query(Bandit).filter(Bandit.project_id == project_id).all()
    if not bandits:
        raise HTTPException(status_code=404, detail="No bandits for this project")

    for _ in range(payload.n_trials):
        samples = [_sample_bandit_draw(b) for b in bandits]
        chosen_idx = int(np.argmax(samples))
        chosen = bandits[chosen_idx]
        reward = float(chosen.price)
        _ = thompson_submit_reward(chosen.bandit_id, SubmitRewardRequest(reward=reward), db=db)
        bandits = db.query(Bandit).filter(Bandit.project_id == project_id).all()

    return {"message": "Simulation finished", "n_trials": payload.n_trials}

@app.get("/projects/{project_id}/thompson/plot", tags=["Thompson"])
def thompson_plot(project_id: int, db: Session = Depends(get_db)):
    """
    Return PNG plot of posterior distributions for bandits in the project.
    """
    bandits = db.query(Bandit).filter(Bandit.project_id == project_id).all()
    if not bandits:
        raise HTTPException(status_code=404, detail="No bandits for this project")

    means = [float(b.mean) for b in bandits]
    stds = [1.0 / np.sqrt(float(b.variance)) for b in bandits]
    xmin = min(means) - 4 * max(stds)
    xmax = max(means) + 4 * max(stds)
    x = np.linspace(xmin, xmax, 400)

    plt.figure(figsize=(10, 5))
    for b in bandits:
        mean = float(b.mean)
        lam = float(b.variance)
        std = 1.0 / np.sqrt(lam) if lam > 0 else 1.0
        y = norm.pdf(x, mean, std)
        plt.plot(x, y, label=f"Price={float(b.price):.2f} | Mean={mean:.2f} | Trials={b.trial}")
    plt.title(f"Posterior distributions — project {project_id}")
    plt.xlabel("Reward")
    plt.ylabel("Density")
    plt.legend()
    plt.grid(True)

    buf = BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    return Response(content=buf.read(), media_type="image/png")
