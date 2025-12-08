# ============================
#   endpoints.py  (COMPLETE)
# ============================

from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    UploadFile,
    File,
    FastAPI,
    Response,
)
from fastapi.staticfiles import StaticFiles      # ✅ NEW
from sqlalchemy.orm import Session
import numpy as np
import os
from io import BytesIO

import matplotlib.pyplot as plt
from scipy.stats import norm

from database.database import get_db
from database.models import Project, Bandit, Experiment

# ---------- REQUEST MODELS ----------
from models.Request.requests import (
    CreateProjectRequest,
    SubmitRewardRequest,
    CreateBanditRequestModel,
)

# ---------- RESPONSE MODELS ----------
from models.Response.responses import (
    CreateProjectResponseModel,
    CreateBanditResponseModel,
    ProjectItem,
    BanditReport,
    ThompsonSelectResponse,
)

# ----------------------------------------------------
#                   ROUTER
# ----------------------------------------------------
router = APIRouter()

# ======================================================
#  CREATE PROJECT
# ======================================================
@router.post("/projects", response_model=CreateProjectResponseModel)
def create_project(request: CreateProjectRequest, db: Session = Depends(get_db)):

    project = Project(
        description=request.description,
        number_bandits=request.number_bandits,
        optimal_price=None,
        last_algorithm_run=None,
    )
    db.add(project)
    db.commit()
    db.refresh(project)

    # Create first bandit
    bandit = Bandit(
        project_id=project.project_id,
        price=request.price,
        mean=0.0,
        variance=1.0,
        reward=0.0,
        trial=0,
        number_explored=0,
    )
    db.add(bandit)
    db.commit()

    return project


# ======================================================
#  UPLOAD PROJECT IMAGE
# ======================================================
@router.post("/projects/{project_id}/upload-image")
def upload_project_image(
    project_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):

    project = db.query(Project).filter_by(project_id=project_id).first()
    if not project:
        raise HTTPException(404, "Project not found")

    # Save under /backend/images (WORKDIR is /backend)
    folder = "/backend/images"
    os.makedirs(folder, exist_ok=True)

    ext = file.filename.split(".")[-1]
    filename = f"project_{project_id}.{ext}"
    path = f"{folder}/{filename}"

    with open(path, "wb") as f:
        f.write(file.file.read())

    # What frontend will use: http://backend:8000 + image_path
    project.image_path = f"/images/{filename}"
    db.commit()

    return {"message": "Image uploaded", "image_path": project.image_path}


# ======================================================
#  GET PROJECTS
# ======================================================
@router.get("/projects", response_model=list[ProjectItem])
def list_projects(db: Session = Depends(get_db)):
    return db.query(Project).order_by(Project.created_at.desc()).all()


# ======================================================
#  CREATE BANDIT
# ======================================================
@router.post("/projects/{project_id}/bandits", response_model=CreateBanditResponseModel)
def create_bandit(
    project_id: int,
    req: CreateBanditRequestModel,
    db: Session = Depends(get_db),
):

    project = db.query(Project).filter_by(project_id=project_id).first()
    if not project:
        raise HTTPException(404, "Project not found")

    bandit = Bandit(
        project_id=project_id,
        price=req.price,
        mean=0.0,
        variance=1.0,
        reward=0.0,
        trial=0,
        number_explored=0,
    )
    db.add(bandit)
    db.commit()
    db.refresh(bandit)

    return bandit


# ======================================================
#  LIST BANDITS
# ======================================================
@router.get("/projects/{project_id}/bandits", response_model=list[BanditReport])
def get_bandits_for_project(project_id: int, db: Session = Depends(get_db)):

    project = db.query(Project).filter_by(project_id=project_id).first()
    if not project:
        raise HTTPException(404, "Project not found")

    return db.query(Bandit).filter_by(project_id=project_id).all()


# ======================================================
#  THOMPSON SELECT
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
        mean = float(b.mean)
        var = max(float(b.variance), 1e-4)
        std = var**0.5
        sample = np.random.normal(mean, std)
        samples.append((b.bandit_id, sample, float(b.price)))

    bandit_id, _, price = max(samples, key=lambda x: x[1])

    project.optimal_price = price
    db.commit()

    return ThompsonSelectResponse(bandit_id=bandit_id, price=price)


# ======================================================
#  THOMPSON POSTERIOR PLOT
# ======================================================
@router.get("/projects/{project_id}/thompson/plot")
def thompson_posterior_plot(project_id: int, db: Session = Depends(get_db)):

    project = db.query(Project).filter_by(project_id=project_id).first()
    if not project:
        raise HTTPException(404, "Project not found")

    bandits = db.query(Bandit).filter_by(project_id=project_id).all()
    if not bandits:
        raise HTTPException(404, "No bandits found")

    means = [float(b.mean) for b in bandits]
    vars_ = [max(float(b.variance), 1e-4) for b in bandits]
    stds = [v**0.5 for v in vars_]

    xmin = min(means) - 4 * max(stds)
    xmax = max(means) + 4 * max(stds)
    x = np.linspace(xmin, xmax, 400)

    plt.figure(figsize=(8, 4))
    for b in bandits:
        mean = float(b.mean)
        var = max(float(b.variance), 1e-4)
        y = norm.pdf(x, mean, var**0.5)
        plt.plot(x, y, label=f"Bandit {b.bandit_id} | price={b.price}")

    plt.legend(fontsize=8)
    plt.grid(True)
    buf = BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)

    return Response(content=buf.read(), media_type="image/png")


# ======================================================
#  UPDATE REWARD
# ======================================================
@router.post("/bandits/{bandit_id}/thompson/reward")
def submit_reward(
    bandit_id: int,
    req: SubmitRewardRequest,
    db: Session = Depends(get_db),
):
    bandit = db.query(Bandit).filter_by(bandit_id=bandit_id).first()
    if not bandit:
        raise HTTPException(404, "Bandit not found")

    # Write experiment record
    experiment = Experiment(
        project_id=bandit.project_id,
        bandit_id=bandit_id,
        reward=req.reward,
        decision=req.decision,
    )
    db.add(experiment)

    # FIXED FLOAT HANDLING
    bandit.reward = float(bandit.reward) + float(req.reward)
    bandit.trial += 1
    bandit.mean = float(bandit.reward) / float(bandit.trial)
    bandit.variance = max(1.0 / float(bandit.trial), 0.0001)

    db.commit()

    return {
        "message": "Reward updated",
        "bandit_id": bandit_id,
        "new_mean": bandit.mean,
    }


# ======================================================
#  FASTAPI APP
# ======================================================
app = FastAPI()

# ✅ Serve /images/* from /backend/images
app.mount("/images", StaticFiles(directory="images"), name="images")

app.include_router(router)