from __future__ import annotations

from collections.abc import Callable

from fastapi import Depends, HTTPException, status

from app.core.security import decode_token, get_user_principal_context, oauth2_scheme
from app.schemas.auth import Principal


def get_current_principal(token: str = Depends(oauth2_scheme)) -> Principal:
    payload = decode_token(token)
    username = payload["sub"]
    try:
        context = get_user_principal_context(username)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found or disabled") from exc
    return Principal(**context)


def require_permissions(*permissions: str) -> Callable:
    def dependency(principal: Principal = Depends(get_current_principal)) -> Principal:
        granted = set(principal.permissions)
        missing = [permission for permission in permissions if permission not in granted]
        if missing:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Missing permissions: {', '.join(missing)}",
            )
        return principal

    return dependency
