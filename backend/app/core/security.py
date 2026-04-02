from __future__ import annotations

from datetime import UTC, datetime, timedelta

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings
from app.core.session_store import create_login_session, revoke_session, validate_session


pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.api_v1_prefix}/auth/token")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_system_user(username: str, password: str) -> dict | None:
    from app.services.management_service import store

    return store.authenticate_system_user(username, password)


def get_user_principal_context(username: str) -> dict:
    from app.services.management_service import store

    return store.get_principal_context(username)


def create_access_token(subject: str, roles: list[str], permissions: list[str], session_id: str, full_name: str | None = None) -> str:
    expires_at = datetime.now(UTC) + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {
        "sub": subject,
        "full_name": full_name or subject,
        "sid": session_id,
        "roles": roles,
        "permissions": permissions,
        "type": "access",
        "exp": expires_at,
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def create_refresh_token(subject: str, roles: list[str], session_id: str) -> str:
    expires_at = datetime.now(UTC) + timedelta(minutes=settings.refresh_token_expire_minutes)
    payload = {
        "sub": subject,
        "sid": session_id,
        "roles": roles,
        "type": "refresh",
        "exp": expires_at,
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def create_token_bundle(subject: str, roles: list[str], permissions: list[str], full_name: str | None = None) -> tuple[str, str]:
    session_id = create_login_session(subject, full_name or subject, roles, permissions)
    return (
        create_access_token(subject, roles, permissions, session_id=session_id, full_name=full_name),
        create_refresh_token(subject, roles, session_id=session_id),
    )


def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        ) from exc
    session_id = payload.get("sid")
    token_type = payload.get("type")
    if not session_id or token_type not in {"access", "refresh"}:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
    session_payload = validate_session(session_id, token_type=token_type)
    if not session_payload or session_payload.get("username") != payload.get("sub"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session expired, please login again")
    return payload


def update_system_user_password(username: str, password: str) -> None:
    from app.services.management_service import store

    store.update_user_password(username, password)


def record_user_login(username: str) -> None:
    from app.services.management_service import store

    store.touch_last_login(username)


def logout_session(token: str) -> None:
    payload = decode_token(token)
    revoke_session(payload["sid"])
