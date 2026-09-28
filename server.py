import base64
import io
import os
from datetime import datetime

import matplotlib.pyplot as plt
from flask import Flask, jsonify, request

from Algorithm import time_complexity_visualizer
from algorithms import ALGORITHMS
from database import Analysis, SessionLocal, init_db

app = Flask(__name__)

SNAPSHOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "snapshots")
os.makedirs(SNAPSHOT_DIR, exist_ok=True)

init_db()


def _validate_params(algo_name, step, n_max):
    """Shared validation for the GET and POST /analyze params.

    Returns (algo_name, step, n_max_value, error_response) where
    error_response is None on success, or a (jsonify(...), 400) tuple to
    return directly on failure.
    """
    if not algo_name:
        return None, None, None, (jsonify(error="Missing required query parameter: algo"), 400)
    algo_name = str(algo_name).strip().strip("'\"").lower()

    if algo_name not in ALGORITHMS:
        return None, None, None, (jsonify(
            error=f"Unknown algorithm '{algo_name}'",
            supported_algorithms=sorted(ALGORITHMS.keys()),
        ), 400)

    if step is None:
        return None, None, None, (jsonify(error="Missing required query parameter: step"), 400)
    try:
        step_value = int(str(step).replace(",", ""))
    except (TypeError, ValueError):
        return None, None, None, (jsonify(error="Query parameter 'step' must be a positive integer"), 400)
    if step_value <= 0:
        return None, None, None, (jsonify(error="Query parameter 'step' must be a positive integer"), 400)

    if n_max is None:
        return None, None, None, (jsonify(error="Missing required query parameter: n_max"), 400)
    try:
        n_max_value = int(str(n_max).replace(",", ""))
    except ValueError:
        return None, None, None, (jsonify(error="Query parameter 'n_max' must be an integer"), 400)

    if n_max_value <= 0:
        return None, None, None, (jsonify(error="Query parameter 'n_max' must be greater than 0"), 400)

    return algo_name, step_value, n_max_value, None


def _run_analysis(algo_name, step_value, n_max_value):
    """Runs the visualizer, saves a PNG snapshot, and returns the response dict."""
    algorithm = ALGORITHMS[algo_name]

    fig, input_sizes, times = time_complexity_visualizer(
        algorithm, n_min=0, n_max=n_max_value, n_step=step_value, algo_name=algo_name
    )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{algo_name}_{timestamp}.png"
    filepath = os.path.join(SNAPSHOT_DIR, filename)
    fig.savefig(filepath, format="png")

    buffer = io.BytesIO()
    fig.savefig(buffer, format="png")
    plt.close(fig)
    buffer.seek(0)
    encoded_image = base64.b64encode(buffer.read()).decode("utf-8")

    return {
        "algo": algo_name,
        "step": step_value,
        "n_min": 0,
        "n_max": n_max_value,
        "input_sizes": input_sizes,
        "times": times,
        "snapshot_path": filepath,
        "image_base64": encoded_image,
    }, timestamp


@app.route("/analyze", methods=["GET"])
def analyze():
    algo_name, step_value, n_max_value, error = _validate_params(
        request.args.get("algo", type=str),
        request.args.get("step", type=str),
        request.args.get("n_max", type=str),
    )
    if error:
        return error

    result, _ = _run_analysis(algo_name, step_value, n_max_value)
    return jsonify(**result)


@app.route("/analyze", methods=["POST"])
def save_analysis():
    body = request.get_json(silent=True) or {}

    algo_name, step_value, n_max_value, error = _validate_params(
        body.get("algo"),
        body.get("step"),
        body.get("n_max"),
    )
    if error:
        return error

    result, _ = _run_analysis(algo_name, step_value, n_max_value)

    with SessionLocal.begin() as session:
        analysis = Analysis(**result)
        session.add(analysis)
        session.flush()
        analysis_id = analysis.id
        created_at = analysis.created_at

    return jsonify(id=analysis_id, created_at=created_at.isoformat(), **result), 201


@app.route("/algorithms", methods=["GET"])
def list_algorithms():
    return jsonify(supported_algorithms=sorted(ALGORITHMS.keys()))


if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)
