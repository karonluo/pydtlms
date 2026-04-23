from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import uuid4

from redis import Redis

from app.core.cache import build_cache_key, get_cache_client
from app.core.config import settings


def _session_key(session_id: str) -> str:
    return build_cache_key("auth", "session", session_id)


def _access_key(session_id: str) -> str:
    return build_cache_key("auth", "session", "access", session_id)


def _refresh_key(session_id: str) -> str:
    return build_cache_key("auth", "session", "refresh", session_id)


def _client() -> Redis:
    return get_cache_client()


def create_login_session(username: str, full_name: str, roles: list[str], permissions: list[str]) -> str:
    session_id = uuid4().hex
    now = datetime.now(UTC)
    payload = {
        "session_id": session_id,
        "username": username,
        "full_name": full_name,
        "roles": roles,
        "permissions": permissions,
        "created_at": now.isoformat(),
        "last_seen_at": now.isoformat(),
        "access_expires_at": (now + timedelta(minutes=settings.access_token_expire_minutes)).isoformat(),
        "refresh_expires_at": (now + timedelta(minutes=settings.refresh_token_expire_minutes)).isoformat(),
    }

    client = _client()
    client.set(_session_key(session_id), json.dumps(payload, ensure_ascii=False), ex=settings.refresh_token_expire_minutes * 60)
    client.set(_access_key(session_id), username, ex=settings.access_token_expire_minutes * 60)
    client.set(_refresh_key(session_id), username, ex=settings.refresh_token_expire_minutes * 60)
    return session_id


def get_session_payload(session_id: str) -> dict | None:
    value = _client().get(_session_key(session_id))
    if not value:
        return None
    if not isinstance(value, (str, bytes, bytearray)):
        return None
    payload: Any = json.loads(value)
    return payload if isinstance(payload, dict) else None


def validate_session(session_id: str, token_type: str) -> dict | None:
    payload = get_session_payload(session_id)
    if not payload:
        return None

    client = _client()
    type_key = _access_key(session_id) if token_type == "access" else _refresh_key(session_id)
    if not client.exists(type_key):
        return None

    payload["last_seen_at"] = datetime.now(UTC).isoformat()
    client.set(_session_key(session_id), json.dumps(payload, ensure_ascii=False), ex=settings.refresh_token_expire_minutes * 60)
    return payload


def revoke_session(session_id: str) -> None:
    client = _client()
    client.delete(_session_key(session_id), _access_key(session_id), _refresh_key(session_id))