from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from decimal import Decimal
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from apscheduler.schedulers.background import BackgroundScheduler
from utils.config import SessionLocal
from db.models import User, Project, Bandit, Experiment
from etl.thompson_engine import run_thompson_for_project, run_thompson_for_all_projects

app = Flask(__name__)
CORS(app)

def serialize_value(v):
    if isinstance(v, Decimal):
        return float(v)
    if isinstance(v, datetime):
        return v.isoformat()
    return v

def to_dict(instance):
    if hasattr(instance, "__table__"):
        return {c.name: serialize_value(getattr(instance, c.name)) for c in instance.__table__.columns}
    return {}

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/auth/register", methods=["POST"])
def register():
    session = SessionLocal()
    try:
        data = request.get_json() or {}
        email = data.get("email")
        password = data.get("password")
        if not email or not password:
            abort(400, description="Missing email or password")
        existing = session.query(User).filter(User.email == email).one_or_none()
        if existing:
            abort(409, description="User already exists")
        user = User(email=email, password_hash=generate_password_hash(password))
        session.add(user)
        session.commit()
        session.refresh(user)
        return jsonify({"user_id": user.user_id, "email": user.email}), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()

@app.route("/auth/login", methods=["POST"])
def login():
    session = SessionLocal()
    try:
        data = request.get_json() or {}
        email = data.get("email")
        password = data.get("password")
        if not email or not password:
            abort(400, description="Missing email or password")
        user = session.query(User).filter(User.email == email).one_or_none()
        if not user or not check_password_hash(user.password_hash, password):
            abort(401, description="Invalid credentials")
        return jsonify({"user_id": user.user_id, "email": user.email}), 200
    finally:
        session.close()

@app.route("/projects", methods=["GET"])
def get_projects():
    session = SessionLocal()
    try:
        projects = session.query(Project).all()
        return jsonify([to_dict(p) for p in projects])
    finally:
        session.close()

@app.route("/projects/<int:project_id>", methods=["GET"])
def get_project(project_id):
    session = SessionLocal()
    try:
        project = session.query(Project).filter(Project.project_id == project_id).one_or_none()
        if not project:
            abort(404, description="Project not found")
        return jsonify(to_dict(project))
    finally:
        session.close()

@app.route("/projects", methods=["POST"])
def create_project():
    session = SessionLocal()
    try:
        data = request.get_json() or {}
        description = data.get("description")
        number_bandits = data.get("number_bandits")
        if not description or number_bandits is None:
            abort(400, description="Missing description or number_bandits")
        project = Project(description=description, number_bandits=number_bandits)
        session.add(project)
        session.commit()
        session.refresh(project)
        return jsonify(to_dict(project)), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()

@app.route("/projects/<int:project_id>", methods=["PUT"])
def update_project(project_id):
    session = SessionLocal()
    try:
        data = request.get_json() or {}
        project = session.query(Project).filter(Project.project_id == project_id).one_or_none()
        if not project:
            abort(404, description="Project not found")
        if "description" in data:
            project.description = data["description"]
        if "number_bandits" in data:
            project.number_bandits = data["number_bandits"]
        session.commit()
        session.refresh(project)
        return jsonify(to_dict(project))
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()

@app.route("/projects/<int:project_id>", methods=["DELETE"])
def delete_project(project_id):
    session = SessionLocal()
    try:
        project = session.query(Project).filter(Project.project_id == project_id).one_or_none()
        if not project:
            abort(404, description="Project not found")
        session.delete(project)
        session.commit()
        return jsonify({"success": True, "message": "Project deleted"})
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()

@app.route("/bandits", methods=["GET"])
def get_bandits():
    session = SessionLocal()
    try:
        bandits = session.query(Bandit).all()
        return jsonify([to_dict(b) for b in bandits])
    finally:
        session.close()

@app.route("/bandits/<int:bandit_id>", methods=["GET"])
def get_bandit(bandit_id):
    session = SessionLocal()
    try:
        bandit = session.query(Bandit).filter(Bandit.bandit_id == bandit_id).one_or_none()
        if not bandit:
            abort(404, description="Bandit not found")
        return jsonify(to_dict(bandit))
    finally:
        session.close()

@app.route("/bandits", methods=["POST"])
def create_bandit():
    session = SessionLocal()
    try:
        data = request.get_json() or {}
        project_id = data.get("project_id")
        price = data.get("price")
        if project_id is None or price is None:
            abort(400, description="Missing project_id or price")
        bandit = Bandit(
            project_id=project_id,
            price=price,
            mean=data.get("mean", 0.0),
            variance=data.get("variance", 1.0),
            reward=data.get("reward", 0.0),
            trial=data.get("trial", 0),
            number_explored=data.get("number_explored", 0),
        )
        session.add(bandit)
        session.commit()
        session.refresh(bandit)
        return jsonify(to_dict(bandit)), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()

@app.route("/bandits/<int:bandit_id>", methods=["PUT"])
def update_bandit(bandit_id):
    session = SessionLocal()
    try:
        data = request.get_json() or {}
        bandit = session.query(Bandit).filter(Bandit.bandit_id == bandit_id).one_or_none()
        if not bandit:
            abort(404, description="Bandit not found")
        for field in ["project_id", "price", "mean", "variance", "reward", "trial", "number_explored"]:
            if field in data:
                setattr(bandit, field, data[field])
        session.commit()
        session.refresh(bandit)
        return jsonify(to_dict(bandit))
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()

@app.route("/bandits/<int:bandit_id>", methods=["DELETE"])
def delete_bandit(bandit_id):
    session = SessionLocal()
    try:
        bandit = session.query(Bandit).filter(Bandit.bandit_id == bandit_id).one_or_none()
        if not bandit:
            abort(404, description="Bandit not found")
        session.delete(bandit)
        session.commit()
        return jsonify({"success": True, "message": "Bandit deleted"})
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()

@app.route("/experiments", methods=["GET"])
def get_experiments():
    session = SessionLocal()
    try:
        experiments = session.query(Experiment).all()
        return jsonify([to_dict(e) for e in experiments])
    finally:
        session.close()

@app.route("/experiments/<int:experiment_id>", methods=["GET"])
def get_experiment(experiment_id):
    session = SessionLocal()
    try:
        experiment = session.query(Experiment).filter(Experiment.experiment_id == experiment_id).one_or_none()
        if not experiment:
            abort(404, description="Experiment not found")
        return jsonify(to_dict(experiment))
    finally:
        session.close()

@app.route("/experiments", methods=["POST"])
def create_experiment():
    session = SessionLocal()
    try:
        data = request.get_json() or {}
        required = ["project_id", "bandit_id", "decision", "reward"]
        if any(k not in data for k in required):
            abort(400, description="Missing required fields")
        experiment = Experiment(
            project_id=data["project_id"],
            bandit_id=data["bandit_id"],
            decision=data["decision"],
            reward=data["reward"],
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
        )
        session.add(experiment)
        session.commit()
        session.refresh(experiment)
        return jsonify(to_dict(experiment)), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()

@app.route("/experiments/<int:experiment_id>", methods=["PUT"])
def update_experiment(experiment_id):
    session = SessionLocal()
    try:
        data = request.get_json() or {}
        experiment = session.query(Experiment).filter(Experiment.experiment_id == experiment_id).one_or_none()
        if not experiment:
            abort(404, description="Experiment not found")
        for field in ["project_id", "bandit_id", "decision", "reward", "start_date", "end_date"]:
            if field in data:
                setattr(experiment, field, data[field])
        session.commit()
        session.refresh(experiment)
        return jsonify(to_dict(experiment))
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()

@app.route("/experiments/<int:experiment_id>", methods=["DELETE"])
def delete_experiment(experiment_id):
    session = SessionLocal()
    try:
        experiment = session.query(Experiment).filter(Experiment.experiment_id == experiment_id).one_or_none()
        if not experiment:
            abort(404, description="Experiment not found")
        session.delete(experiment)
        session.commit()
        return jsonify({"success": True, "message": "Experiment deleted"})
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()

@app.route("/algorithm/run/<int:project_id>", methods=["POST"])
def algorithm_run_project(project_id):
    data = request.get_json() or {}
    strategy = data.get("strategy", "bernoulli")
    create_experiment = bool(data.get("create_experiment", False))
    try:
        result = run_thompson_for_project(project_id, strategy=strategy, persist=True, create_experiment=create_experiment)
        if result is None:
            abort(404, description="Project or bandits not found")
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/algorithm/run_all", methods=["POST"])
def algorithm_run_all():
    data = request.get_json() or {}
    strategy = data.get("strategy", "bernoulli")
    create_experiment = bool(data.get("create_experiment", False))
    try:
        results = run_thompson_for_all_projects(strategy=strategy, persist=True, create_experiment=create_experiment)
        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/algorithm/optimal_price/<int:project_id>", methods=["GET"])
def algorithm_optimal_price(project_id):
    session = SessionLocal()
    try:
        project = session.query(Project).filter(Project.project_id == project_id).one_or_none()
        if not project:
            abort(404, description="Project not found")
        return jsonify(
            {
                "project_id": project.project_id,
                "description": project.description,
                "optimal_price": serialize_value(project.optimal_price),
                "last_algorithm_run": serialize_value(project.last_algorithm_run),
            }
        )
    finally:
        session.close()

scheduler = BackgroundScheduler(daemon=True)

def scheduled_thompson():
    run_thompson_for_all_projects(strategy="bernoulli", persist=True, create_experiment=False)

scheduler.add_job(scheduled_thompson, "interval", minutes=10)
scheduler.start()
