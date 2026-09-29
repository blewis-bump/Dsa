"""JWT authentication: creating tokens at login and checking them on requests.

How it works:
1. A user sends their username and password to POST /login.
2. If they match AUTHORIZED_USERS, the server returns a signed JWT.
3. The user sends that JWT on protected requests in this header:
       Authorization: Bearer <token>
4. The @jwt_required decorator checks the header before the endpoint runs.
"""
import hmac
from datetime import datetime, timedelta, timezone
from functools import wraps

import jwt
from flask import g, jsonify, request

import config

UNAUTHORIZED_MESSAGE = "I don't know you"


def check_credentials(username, password):
    """Return True if the username exists and the password matches."""
    if not isinstance(username, str) or not isinstance(password, str):
        return False
    expected_password = config.AUTHORIZED_USERS.get(username)
    if expected_password is None:
        return False
    # compare_digest takes the same time whether or not the values match,
    # so attackers can't guess the password one character at a time.
    return hmac.compare_digest(password.encode(), expected_password.encode())


def create_token(username):
    """Create a signed JWT for this user that expires after JWT_EXPIRES_MINUTES."""
    now = datetime.now(timezone.utc)
    payload = {
        "sub": username,  # "subject": who the token belongs to
        "iat": now,       # "issued at"
        "exp": now + timedelta(minutes=config.JWT_EXPIRES_MINUTES),
    }
    return jwt.encode(payload, config.JWT_SECRET_KEY, algorithm=config.JWT_ALGORITHM)


def get_user_from_token(token):
    """Return the username inside a valid token, or None if the token is bad.

    A token is bad if its signature is wrong, it has expired, it is malformed,
    or its user is no longer in AUTHORIZED_USERS.
    """
    try:
        payload = jwt.decode(
            token,
            config.JWT_SECRET_KEY,
            algorithms=[config.JWT_ALGORITHM],
            options={"require": ["sub", "exp"]},
        )
    except jwt.InvalidTokenError:
        return None

    username = payload["sub"]
    if username not in config.AUTHORIZED_USERS:
        return None
    return username


def _read_bearer_token():
    """Pull the token out of 'Authorization: Bearer <token>', or return None."""
    header = request.headers.get("Authorization", "")
    scheme, _, token = header.partition(" ")
    if scheme.lower() != "bearer" or not token.strip():
        return None
    return token.strip()


def unauthorized_response():
    response = jsonify(error=UNAUTHORIZED_MESSAGE)
    response.headers["WWW-Authenticate"] = "Bearer"
    return response, 401


def jwt_required(endpoint):
    """Decorator: only run the endpoint if the request has a valid JWT.

    On success the username is available inside the endpoint as g.current_user.
    """
    @wraps(endpoint)
    def wrapper(*args, **kwargs):
        token = _read_bearer_token()
        username = get_user_from_token(token) if token else None
        if username is None:
            return unauthorized_response()

        g.current_user = username
        return endpoint(*args, **kwargs)

    return wrapper
