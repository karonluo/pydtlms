from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.rbac import get_current_principal
from app.core.security import (
    authenticate_system_user,
    create_token_bundle,
    logout_session,
    record_user_login,
    update_system_user_password,
    oauth2_scheme,
)
from app.schemas.auth import PasswordChangeRequest, Principal, TokenResponse, UserProfile, UserProfileUpdate
from app.services.management_service import store


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends()) -> TokenResponse:
    user = authenticate_system_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    record_user_login(form_data.username)
    access_token, refresh_token = create_token_bundle(
        user["username"],
        user["roles"],
        user["permissions"],
        full_name=user["full_name"],
    )
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.get("/me", response_model=Principal)
def me(principal: Principal = Depends(get_current_principal)) -> Principal:
    return principal


@router.get("/profile", response_model=UserProfile)
def profile(principal: Principal = Depends(get_current_principal)) -> UserProfile:
    try:
        return store.get_profile(principal.username)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found") from exc


@router.put("/profile", response_model=UserProfile)
def update_profile(payload: UserProfileUpdate, principal: Principal = Depends(get_current_principal)) -> UserProfile:
    return store.update_profile(principal.username, payload)


@router.post("/change-password")
def change_password(payload: PasswordChangeRequest, principal: Principal = Depends(get_current_principal)) -> dict[str, str]:
    user = authenticate_system_user(principal.username, payload.current_password)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current password is incorrect")
    update_system_user_password(principal.username, payload.new_password)
    return {"message": "Password updated"}


@router.post("/logout")
def logout(token: str = Depends(oauth2_scheme), principal: Principal = Depends(get_current_principal)) -> dict[str, str]:
    logout_session(token)
    return {"message": "Logged out"}
