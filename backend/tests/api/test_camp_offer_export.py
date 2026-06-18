"""Tests for the GET /recruitment/camp-offers/export endpoint."""

from __future__ import annotations

import sys
import pathlib
from typing import Any

import pytest
from fastapi.testclient import TestClient


BACKEND_DIR = pathlib.Path(__file__).resolve().parents[2]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.main import app  # noqa: E402
from app.api.v1 import recruitment as recruitment_api  # noqa: E402


@pytest.fixture
def client() -> TestClient:
    with TestClient(app) as test_client:
        yield test_client


def _install_principal(monkeypatch, subject: str, permissions: list[str]) -> str:
    access_token = f"token-{subject}"

    def fake_decode_token(token: str) -> dict[str, str]:
        if token != access_token:
            raise AssertionError(f"Unexpected token: {token}")
        return {"sub": subject}

    def fake_get_user_principal_context(username: str) -> dict[str, Any]:
        assert username == subject
        return {
            "username": subject,
            "full_name": "测试用户",
            "roles": ["recruitment_admin"],
            "permissions": permissions,
        }

    monkeypatch.setattr("app.core.rbac.decode_token", fake_decode_token)
    monkeypatch.setattr(
        "app.core.rbac.get_user_principal_context", fake_get_user_principal_context
    )
    return access_token


def test_export_camp_offers_returns_xlsx_with_matching_rows(monkeypatch, client: TestClient) -> None:
    access_token = _install_principal(monkeypatch, "recruiter", ["recruitment_camp_offer:read"])

    fake_rows = [
        {
            "candidate_no": "SH1",
            "student_name": "张三",
            "plan_name": "2026 计划",
            "student_email": "z@example.com",
            "student_phone": "13800000000",
            "first_choice_advisor_name": "导师甲",
            "first_choice_advisor_team_name": "团队A",
            "first_choice_screening_score": 88.5,
            "second_choice_advisor_name": "导师乙",
            "second_choice_advisor_team_name": "团队B",
            "second_choice_screening_score": 75.0,
            "is_agree": True,
            "is_sent_mail": False,
            "reason": "",
            "student_offer_submitted_at": None,
            "created_at": "2026-06-01T10:00:00",
        }
    ]

    monkeypatch.setattr(
        recruitment_api, "export_camp_offers",
        lambda **kwargs: fake_rows,
    )

    response = client.get(
        "/api/v1/recruitment/camp-offers/export",
        headers={"Authorization": f"Bearer {access_token}"},
        params={"keyword": "张三", "plan_id": 5},
    )

    assert response.status_code == 200
    assert response.headers["content-type"].startswith(
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    disposition = response.headers.get("content-disposition", "")
    assert "attachment" in disposition
    assert ".xlsx" in disposition
    # The body must be a valid xlsx zip (starts with "PK")
    assert response.content[:2] == b"PK"


def test_export_camp_offers_forwards_filters(monkeypatch, client: TestClient) -> None:
    access_token = _install_principal(monkeypatch, "recruiter", ["recruitment_camp_offer:read"])

    captured: dict[str, Any] = {}

    def fake_export(**kwargs):
        captured.update(kwargs)
        return []

    monkeypatch.setattr(recruitment_api, "export_camp_offers", fake_export)

    response = client.get(
        "/api/v1/recruitment/camp-offers/export",
        headers={"Authorization": f"Bearer {access_token}"},
        params={"keyword": "SH2027", "plan_id": 7, "is_sent_mail": "true", "is_agree": "false"},
    )

    assert response.status_code == 200
    assert captured["keyword"] == "SH2027"
    assert captured["plan_id"] == 7
    assert captured["is_sent_mail"] is True
    assert captured["is_agree"] is False
