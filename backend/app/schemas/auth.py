from pydantic import BaseModel


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class Principal(BaseModel):
    username: str
    full_name: str
    roles: list[str]
    permissions: list[str]


class UserProfile(BaseModel):
    username: str
    full_name: str
    role_name: str
    department_name: str
    phone_number: str | None = None
    email: str | None = None
    theme_color: str


class UserProfileUpdate(BaseModel):
    full_name: str
    phone_number: str | None = None
    email: str | None = None
    theme_color: str


class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str
