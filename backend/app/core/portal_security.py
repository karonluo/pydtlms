from __future__ import annotations

from datetime import UTC, datetime, timedelta

from fastapi import HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from app.core.config import settings


PORTAL_TOKEN_PREFIX = "portal-student:"
portal_bearer = HTTPBearer(auto_error=False)


def create_portal_access_token(student_id: int, full_name: str) -> str:
    expires_at = datetime.now(UTC) + timedelta(days=7)
    payload = {
        "sub": f"{PORTAL_TOKEN_PREFIX}{student_id}",
        "full_name": full_name,
        "type": "portal",
        "exp": expires_at,
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def decode_portal_access_token(token: str) -> int:
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    except JWTError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired portal token") from exc
    subject = str(payload.get("sub") or "")
    if payload.get("type") != "portal" or not subject.startswith(PORTAL_TOKEN_PREFIX):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid portal token")
    return int(subject.removeprefix(PORTAL_TOKEN_PREFIX))


def resolve_portal_student_id(credentials: HTTPAuthorizationCredentials | None) -> int:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Portal authentication required")
    return decode_portal_access_token(credentials.credentials)