"""Demo JWT authentication helpers for the portfolio API."""
from datetime import datetime, timedelta, timezone
import hashlib
import os
import secrets

SECRET_KEY = os.getenv("JWT_SECRET", "change-me-in-production")
TOKEN_TTL_MINUTES = int(os.getenv("TOKEN_TTL_MINUTES", "60"))


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def create_token(username: str) -> str:
    expires = int((datetime.now(timezone.utc) + timedelta(minutes=TOKEN_TTL_MINUTES)).timestamp())
    nonce = secrets.token_hex(8)
    payload = f"{username}.{expires}.{nonce}"
    signature = hashlib.sha256(f"{SECRET_KEY}.{payload}".encode()).hexdigest()
    return f"{payload}.{signature}"


def verify_token(token: str) -> str | None:
    try:
        username, expires, nonce, signature = token.split(".")
        payload = f"{username}.{expires}.{nonce}"
        expected = hashlib.sha256(f"{SECRET_KEY}.{payload}".encode()).hexdigest()
        if not secrets.compare_digest(signature, expected) or int(expires) < int(datetime.now(timezone.utc).timestamp()):
            return None
        return username
    except (ValueError, TypeError):
        return None
