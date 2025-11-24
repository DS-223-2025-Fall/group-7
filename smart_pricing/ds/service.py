import os
from flask import Flask, request, jsonify, abort
from ds.thompson_engine import run_thompson_for_project, run_thompson_for_all_projects
from core import create_engine_from_env, Base

engine = create_engine_from_env()


app = Flask(__name__)

@app.route("/thompson/run/<int:project_id>", methods=["POST"])
def thompson_run_project(project_id):
    data = request.get_json() or {}
    strategy = data.get("strategy", "bernoulli")
    persist = bool(data.get("persist", True))
    create_experiment = bool(data.get("create_experiment", False))

    try:
        result = run_thompson_for_project(
            project_id,
            strategy=strategy,
            persist=persist,
            create_experiment=create_experiment,
        )
        if result is None:
            abort(404, description="Project or bandits not found")
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/thompson/run_all", methods=["POST"])
def thompson_run_all():
    data = request.get_json() or {}
    strategy = data.get("strategy", "bernoulli")
    persist = bool(data.get("persist", True))
    create_experiment = bool(data.get("create_experiment", False))

    try:
        results = run_thompson_for_all_projects(
            strategy=strategy,
            persist=persist,
            create_experiment=create_experiment,
        )
        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    port = int(os.getenv("DS_PORT", "8888"))
    app.run(host="0.0.0.0", port=port)
