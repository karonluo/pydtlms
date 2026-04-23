from __future__ import annotations

import re

_CHINA_MOBILE_PHONE_PATTERN = re.compile(r"^1[3-9]\d{9}$")
_EMAIL_PATTERN = re.compile(
    r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+$"
)


def normalize_phone_number(value: str) -> str:
    return str(value or "").strip()


def normalize_email(value: str) -> str:
    return str(value or "").strip()


def validate_phone_number(value: str, field_label: str = "手机号") -> str:
    normalized = normalize_phone_number(value)
    if not normalized:
        raise ValueError(f"{field_label}不能为空")
    if not _CHINA_MOBILE_PHONE_PATTERN.fullmatch(normalized):
        raise ValueError(f"{field_label}格式不正确，请输入有效的中国大陆手机号")
    return normalized


def validate_optional_phone_number(value: str | None, field_label: str = "手机号") -> str | None:
    normalized = normalize_phone_number(value or "")
    if not normalized:
        return None
    return validate_phone_number(normalized, field_label)


def validate_email(value: str, field_label: str = "邮箱") -> str:
    normalized = normalize_email(value)
    if not normalized:
        raise ValueError(f"{field_label}不能为空")
    if not _EMAIL_PATTERN.fullmatch(normalized):
        raise ValueError(f"{field_label}格式不正确，请输入有效的邮箱地址")
    return normalized


def validate_optional_email(value: str | None, field_label: str = "邮箱") -> str | None:
    normalized = normalize_email(value or "")
    if not normalized:
        return None
    return validate_email(normalized, field_label)