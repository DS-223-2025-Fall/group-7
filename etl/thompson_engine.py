import random
from typing import Dict, Literal, Optional, Tuple
from datetime import datetime
from utils.config import SessionLocal
from db.models import Project, Bandit, Experiment, get_yerevan_time

Strategy = Literal["bernoulli", "gaussian"]

def _bernoulli_score(bandit: Bandit) -> float:
    successes = float(bandit.reward or 0.0)
    trials = int(bandit.trial or 0)
    failures = max(trials - successes, 0.0)
    alpha = 1.0 + successes
    beta = 1.0 + failures
    return random.betavariate(alpha, beta)

def _gaussian_score(bandit: Bandit) -> float:
    mean = float(bandit.mean or 0.0)
    variance = float(bandit.variance or 1.0)
    variance = max(variance, 1e-6)
    sigma = variance ** 0.5
    return random.gauss(mean, sigma)

def run_thompson_for_project(project_id: int, strategy: Strategy = "bernoulli", persist: bool = False, create_experiment: bool = False) -> Optional[Dict]:
    session = SessionLocal()
    try:
        project = session.query(Project).filter(Project.project_id == project_id).one_or_none()
        if project is None:
            return None
        bandits = session.query(Bandit).filter(Bandit.project_id == project_id).all()
        if not bandits:
            return None
        best_bandit = None
        best_score = None
        for b in bandits:
            if strategy == "gaussian":
                score = _gaussian_score(b)
            else:
                score = _bernoulli_score(b)
            if best_score is None or score > best_score:
                best_score = score
                best_bandit = b
        if best_bandit is None:
            return None
        optimal_price = float(best_bandit.price)
        now = get_yerevan_time()
        if persist:
            project.optimal_price = optimal_price
            project.last_algorithm_run = now
        if create_experiment:
            exp = Experiment(
                project_id=project.project_id,
                bandit_id=best_bandit.bandit_id,
                decision=f"TS_{strategy}",
                reward=0.0,
                start_date=now,
                end_date=now,
            )
            session.add(exp)
        session.commit()
        return {
            "project_id": project.project_id,
            "bandit_id": best_bandit.bandit_id,
            "optimal_price": optimal_price,
            "strategy": strategy,
            "last_algorithm_run": now.isoformat(),
        }
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

def run_thompson_for_all_projects(strategy: Strategy = "bernoulli", persist: bool = False, create_experiment: bool = False) -> Dict[int, Dict]:
    session = SessionLocal()
    try:
        project_ids = [p.project_id for p in session.query(Project.project_id).all()]
    finally:
        session.close()
    results: Dict[int, Dict] = {}
    for pid in project_ids:
        res = run_thompson_for_project(pid, strategy=strategy, persist=persist, create_experiment=create_experiment)
        if res is not None:
            results[pid] = res
    return results
