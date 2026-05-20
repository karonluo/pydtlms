from pydantic import BaseModel, field_validator

from app.schemas.contact import validate_optional_email, validate_optional_phone_number


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
    introduction: str | None = None
    phone_number: str | None = None
    email: str | None = None
    theme_color: str


class UserProfileUpdate(BaseModel):
    full_name: str
    phone_number: str | None = None
    email: str | None = None
    theme_color: str

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number_field(cls, value: str | None) -> str | None:
        return validate_optional_phone_number(value)

    @field_validator("email")
    @classmethod
    def validate_email_field(cls, value: str | None) -> str | None:
        return validate_optional_email(value)


class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str
