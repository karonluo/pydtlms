from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import UTC, datetime, timedelta

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings


pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.api_v1_prefix}/auth/token")


@dataclass(frozen=True)
class BootstrapUser:
    username: str
    full_name: str
    password_hash: str
    roles: list[str]
    permissions: list[str]


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


BOOTSTRAP_USERS: dict[str, BootstrapUser] = {
    settings.demo_admin_username: BootstrapUser(
        username=settings.demo_admin_username,
        full_name="系统管理员",
        password_hash=get_password_hash(settings.demo_admin_password),
        roles=["platform_admin"],
        permissions=[
            "dashboard:read",
            "recruitment:read",
            "recruitment:write",
            "students:read",
            "students:write",
            "training:read",
            "training:write",
            "degree:read",
            "degree:write",
            "audit:read",
            "audit:write",
            "system:read",
            "system:write",
            "workflow:read",
            "workflow:write",
        ],
    ),
    "mentor.demo": BootstrapUser(
        username="mentor.demo",
        full_name="导师示例账号",
        password_hash=get_password_hash("Mentor@123456"),
        roles=["advisor"],
        permissions=["dashboard:read", "students:read", "training:read", "degree:read", "workflow:read"],
    ),
}


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_bootstrap_user(username: str, password: str) -> BootstrapUser | None:
    candidate = BOOTSTRAP_USERS.get(username)
    if candidate and verify_password(password, candidate.password_hash):
        return candidate
    return None


def create_access_token(subject: str, roles: list[str], permissions: list[str], full_name: str | None = None) -> str:
    expires_at = datetime.now(UTC) + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {
        "sub": subject,
        "full_name": full_name or subject,
        "roles": roles,
        "permissions": permissions,
        "type": "access",
        "exp": expires_at,
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def create_refresh_token(subject: str, roles: list[str]) -> str:
    expires_at = datetime.now(UTC) + timedelta(minutes=settings.refresh_token_expire_minutes)
    payload = {
        "sub": subject,
        "roles": roles,
        "type": "refresh",
        "exp": expires_at,
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        ) from exc


def update_bootstrap_user_password(username: str, password: str) -> None:
    candidate = BOOTSTRAP_USERS.get(username)
    if not candidate:
        raise KeyError(username)
    BOOTSTRAP_USERS[username] = replace(candidate, password_hash=get_password_hash(password))
