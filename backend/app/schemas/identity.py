from __future__ import annotations

import re
from datetime import datetime

_CHINA_ID_18_PATTERN = re.compile(r"^\d{17}[\dX]$")
_CHINA_ID_15_PATTERN = re.compile(r"^\d{15}$")
_CHINA_ID_WEIGHTS = (7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2)
_CHINA_ID_CHECKSUM_MAP = "10X98765432"


def normalize_china_resident_id_number(value: str) -> str:
    return str(value or "").strip().upper()


def _is_valid_birth_date(text: str, legacy: bool = False) -> bool:
    try:
        candidate = f"19{text}" if legacy else text
        datetime.strptime(candidate, "%Y%m%d")
    except ValueError:
        return False
    return True


def is_valid_china_resident_id_number(value: str) -> bool:
    normalized = normalize_china_resident_id_number(value)
    if _CHINA_ID_18_PATTERN.fullmatch(normalized):
        if not _is_valid_birth_date(normalized[6:14]):
            return False
        checksum_index = sum(int(char) * weight for char, weight in zip(normalized[:17], _CHINA_ID_WEIGHTS)) % 11
        return normalized[-1] == _CHINA_ID_CHECKSUM_MAP[checksum_index]
    if _CHINA_ID_15_PATTERN.fullmatch(normalized):
        return _is_valid_birth_date(normalized[6:12], legacy=True)
    return False


def validate_china_resident_id_number(value: str, field_label: str = "身份证号") -> str:
    normalized = normalize_china_resident_id_number(value)
    if not normalized:
        raise ValueError(f"{field_label}不能为空")
    if not is_valid_china_resident_id_number(normalized):
        raise ValueError(f"{field_label}格式不正确，请输入有效的中国居民身份证号码")
    return normalized