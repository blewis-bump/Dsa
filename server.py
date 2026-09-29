"""Flask API for the Time Complexity Visualizer.

Endpoints:
    GET  /algorithms  - list the algorithm names you can analyze (public)
    GET  /analyze     - time an algorithm and return the chart (public)
    POST /login       - exchange username + password for a JWT
    POST /analyze     - same as GET, but also saves the result (requires a JWT)

Run it with:  python server.py
"""
from flask import Flask, jsonify, request

from algorithms import ALGORITHMS
from auth import check_credentials, create_token, jwt_required
from database import init_db, store_analysis
from validation import ValidationError, parse_analysis_params
from visualizer import run_analysis

app = Flask(__name__)
init_db()


@app.errorhandler(ValidationError)
def handle_validation_error(error):
    """Any ValidationError raised in an endpoint becomes a 400 JSON response."""
    return jsonify(error=error.message, **error.extra), 400


def _read_json_body():
    """Return the request's JSON body as a dict ({} if it's missing or not an object)."""
    body = request.get_json(silent=True)
    return body if isinstance(body, dict) else {}


@app.get("/algorithms")
def list_algorithms():
    return jsonify(supported_algorithms=sorted(ALGORITHMS))


@app.get("/analyze")
def analyze():
    params = parse_analysis_params(
        request.args.get("algo"),
        request.args.get("step"),
        request.args.get("n_max"),
    )
    return jsonify(run_analysis(params))


@app.post("/login")
def login():
    body = _read_json_body()
    username = body.get("username")
    if not check_credentials(username, body.get("password")):
        return jsonify(error="Invalid username or password"), 401

    return jsonify(access_token=create_token(username), token_type="Bearer")


@app.post("/analyze")
@jwt_required
def save_analysis():
    body = _read_json_body()
    params = parse_analysis_params(body.get("algo"), body.get("step"), body.get("n_max"))

    result = run_analysis(params)
    saved = store_analysis(result)

    return jsonify(id=saved.id, created_at=saved.created_at.isoformat(), **result), 201


if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)
