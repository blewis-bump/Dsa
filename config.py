"""All project settings live here, so there is one place to look and change them.

Each setting can be overridden with an environment variable of the same name,
e.g. in PowerShell:  $env:JWT_SECRET_KEY = "something-long-and-random"
"""
import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

# Where chart PNGs are written.
SNAPSHOT_DIR = os.environ.get("SNAPSHOT_DIR", os.path.join(PROJECT_DIR, "snapshots"))

# Any SQLAlchemy URL works; the default is a SQLite file next to this script.
DATABASE_URL = os.environ.get(
    "DATABASE_URL", "sqlite:///" + os.path.join(PROJECT_DIR, "analyses.db")
)

# --- JWT settings ---
# The secret signs every token. Anyone who knows it can create valid tokens,
# so always set a real one via the environment outside local development.
JWT_SECRET_KEY = os.environ.get(
    "JWT_SECRET_KEY", "dev-only-secret-change-me-0123456789abcdef"
)
JWT_ALGORITHM = "HS256"
JWT_EXPIRES_MINUTES = int(os.environ.get("JWT_EXPIRES_MINUTES", "60"))

# Users allowed to log in and save analyses: {username: password}.
AUTHORIZED_USERS = {
    os.environ.get("ADMIN_USERNAME", "admin"): os.environ.get("ADMIN_PASSWORD", "admin123"),
}
