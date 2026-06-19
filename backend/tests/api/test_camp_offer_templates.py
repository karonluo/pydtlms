"""Tests for the camp-offer template management endpoints."""

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
from app.services import camp_offer_notification_service  # noqa: E402


@pytest.fixture
def client(tmp_path, monkeypatch) -> TestClient:
    """Wire a temporary offer-template upload dir so the tests do not pollute
    the real ``frontend/public/recruitment/offer-templates`` directory."""

    upload_dir = tmp_path / "offer-templates"
    upload_dir.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(recruitment_api, "OFFER_TEMPLATE_UPLOAD_DIR", upload_dir, raising=False)
    monkeypatch.setattr(
        camp_offer_notification_service, "OFFER_TEMPLATE_UPLOAD_DIR", upload_dir
    )
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


def test_list_offer_templates_returns_builtin_and_uploaded(client: TestClient, monkeypatch) -> None:
    access_token = _install_principal(monkeypatch, "recruiter", ["recruitment_camp_offer:read"])

    upload_dir = recruitment_api.OFFER_TEMPLATE_UPLOAD_DIR
    target = upload_dir / "offer-abcd1234.md"
    target.write_text("# Custom template", encoding="utf-8")

    response = client.get(
        "/api/v1/recruitment/camp-offers/templates",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200
    payload = response.json()
    items = payload["items"]
    sources = [item["source"] for item in items]
    assert sources.count("builtin") == 2
    assert sources.count("uploaded") == 1

    builtin_keys = {item["builtin_key"] for item in items if item["source"] == "builtin"}
    assert builtin_keys == {"first", "second"}

    uploaded = next(item for item in items if item["source"] == "uploaded")
    assert uploaded["filename"] == "offer-abcd1234.md"
    assert uploaded["id"] == "abcd1234"


def test_upload_offer_template_rejects_non_md(client: TestClient, monkeypatch) -> None:
    access_token = _install_principal(
        monkeypatch, "recruiter", ["recruitment_camp_offer:read", "recruitment_camp_offer:write"]
    )

    response = client.post(
        "/api/v1/recruitment/camp-offers/templates",
        headers={"Authorization": f"Bearer {access_token}"},
        files={"file": ("note.txt", b"hello", "text/plain")},
    )

    assert response.status_code == 400
    assert ".md" in response.json()["detail"]


def test_upload_offer_template_rejects_oversize(client: TestClient, monkeypatch) -> None:
    access_token = _install_principal(
        monkeypatch, "recruiter", ["recruitment_camp_offer:read", "recruitment_camp_offer:write"]
    )

    big = b"# x\n" + (b"a" * (1024 * 1024 + 1))
    response = client.post(
        "/api/v1/recruitment/camp-offers/templates",
        headers={"Authorization": f"Bearer {access_token}"},
        files={"file": ("big.md", big, "text/markdown")},
    )

    assert response.status_code == 400
    assert "1 MB" in response.json()["detail"]


def test_upload_offer_template_persists_file(client: TestClient, monkeypatch) -> None:
    access_token = _install_principal(
        monkeypatch, "recruiter", ["recruitment_camp_offer:read", "recruitment_camp_offer:write"]
    )

    response = client.post(
        "/api/v1/recruitment/camp-offers/templates",
        headers={"Authorization": f"Bearer {access_token}"},
        files={"file": ("welcome.md", "# Welcome {candidate_no}", "text/markdown")},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["source"] == "uploaded"
    assert body["filename"].endswith(".md")
    upload_dir = recruitment_api.OFFER_TEMPLATE_UPLOAD_DIR
    on_disk = list(upload_dir.glob("offer-*.md"))
    assert len(on_disk) == 1
    assert on_disk[0].read_text(encoding="utf-8") == "# Welcome {candidate_no}"


def test_delete_uploaded_template_removes_file(client: TestClient, monkeypatch) -> None:
    access_token = _install_principal(
        monkeypatch, "recruiter", ["recruitment_camp_offer:read", "recruitment_camp_offer:write"]
    )
    upload_dir = recruitment_api.OFFER_TEMPLATE_UPLOAD_DIR
    target = upload_dir / "offer-deadbeef.md"
    target.write_text("hello", encoding="utf-8")

    response = client.delete(
        "/api/v1/recruitment/camp-offers/templates/deadbeef",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 204
    assert not target.exists()


def test_delete_builtin_template_rejected(client: TestClient, monkeypatch) -> None:
    access_token = _install_principal(
        monkeypatch, "recruiter", ["recruitment_camp_offer:read", "recruitment_camp_offer:write"]
    )

    response = client.delete(
        "/api/v1/recruitment/camp-offers/templates/first",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 400
    assert "内置" in response.json()["detail"]


def test_offer_template_preview_returns_html_for_uploaded(client: TestClient, monkeypatch) -> None:
    access_token = _install_principal(
        monkeypatch, "recruiter", ["recruitment_camp_offer:read", "recruitment_camp_offer:write"]
    )
    upload_dir = recruitment_api.OFFER_TEMPLATE_UPLOAD_DIR
    target = upload_dir / "offer-cafebabe.md"
    target.write_text("# Hello {student_name}", encoding="utf-8")

    response = client.get(
        "/api/v1/recruitment/camp-offers/templates/cafebabe/preview",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    body = response.text
    assert "<h1>" in body
    assert "张三" in body


def test_send_notification_with_template_id_uses_uploaded_file(
    client: TestClient, monkeypatch
) -> None:
    access_token = _install_principal(
        monkeypatch, "recruiter", ["recruitment_camp_offer:read", "recruitment_camp_offer:write"]
    )
    upload_dir = recruitment_api.OFFER_TEMPLATE_UPLOAD_DIR
    target = upload_dir / "offer-12345678.md"
    target.write_text("# Welcome {student_name}", encoding="utf-8")

    captured: dict[str, Any] = {}

    def fake_run(cmd, **kwargs):
        from pathlib import Path as _Path
        captured["cmd"] = cmd
        captured["cwd"] = kwargs.get("cwd")
        # Drop a fake result file so the response builder is happy.
        for index, item in enumerate(cmd):
            if item == "--result-json":
                result_path = _Path(cmd[index + 1])
                result_path.parent.mkdir(parents=True, exist_ok=True)
                result_path.write_text(
                    "{\"success_count\": 0, \"failure_count\": 1, \"results\": ["
                    "{\"candidate_no\": \"SH1\", \"email\": \"\", \"status\": \"missing\", \"error\": \"not_found\"}]}",
                    encoding="utf-8",
                )
                break
        class _Result:
            returncode = 0
            stdout = ""
            stderr = ""
        return _Result()

    monkeypatch.setattr(camp_offer_notification_service.subprocess, "run", fake_run)

    response = client.post(
        "/api/v1/recruitment/camp-offers/notify",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "candidate_nos": ["SH1"],
            "choice": "first",
            "template_id": "12345678",
            "simulate": False,
        },
    )

    assert response.status_code == 200
    cmd = captured["cmd"]
    assert "--offer-md" in cmd
    offer_md_index = cmd.index("--offer-md")
    assert cmd[offer_md_index + 1] == str(target)
    assert response.json()["template_path"].endswith("offer-12345678.md")


def test_send_notification_falls_back_to_choice_when_no_template_id(
    client: TestClient, monkeypatch
) -> None:
    access_token = _install_principal(
        monkeypatch, "recruiter", ["recruitment_camp_offer:read", "recruitment_camp_offer:write"]
    )

    captured: dict[str, Any] = {}

    def fake_run(cmd, **kwargs):
        from pathlib import Path as _Path
        captured["cmd"] = cmd
        for index, item in enumerate(cmd):
            if item == "--result-json":
                result_path = _Path(cmd[index + 1])
                result_path.parent.mkdir(parents=True, exist_ok=True)
                result_path.write_text(
                    "{\"success_count\": 0, \"failure_count\": 0, \"results\": []}",
                    encoding="utf-8",
                )
                break
        class _Result:
            returncode = 0
            stdout = ""
            stderr = ""
        return _Result()

    monkeypatch.setattr(camp_offer_notification_service.subprocess, "run", fake_run)

    response = client.post(
        "/api/v1/recruitment/camp-offers/notify",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "candidate_nos": ["SH1"],
            "choice": "second",
            "simulate": False,
        },
    )

    assert response.status_code == 200
    cmd = captured["cmd"]
    # No --offer-md when the request defers to the builtin choice.
    assert "--offer-md" not in cmd


def test_send_notification_accepts_hex_template_id(
    client: TestClient, monkeypatch
) -> None:
    """Regression: uploaded templates are stored on disk with a
    ``offer-<hex>.md`` filename, and the upload endpoint returns the hex
    string verbatim as ``id``. The schema validator must accept the hex
    token instead of trying to ``int()``-coerce it (which would raise and
    surface as the unhelpful ``[object Object]`` toast)."""
    access_token = _install_principal(
        monkeypatch, "recruiter", ["recruitment_camp_offer:read", "recruitment_camp_offer:write"]
    )
    upload_dir = recruitment_api.OFFER_TEMPLATE_UPLOAD_DIR
    hex_id = "29c284be97a0425288db3c4da0312bc5"
    target = upload_dir / f"offer-{hex_id}.md"
    target.write_text("# Hex {student_name}", encoding="utf-8")

    captured: dict[str, Any] = {}

    def fake_run(cmd, **kwargs):
        from pathlib import Path as _Path
        captured["cmd"] = cmd
        for index, item in enumerate(cmd):
            if item == "--result-json":
                result_path = _Path(cmd[index + 1])
                result_path.parent.mkdir(parents=True, exist_ok=True)
                result_path.write_text(
                    "{\"success_count\": 0, \"failure_count\": 0, \"results\": []}",
                    encoding="utf-8",
                )
                break
        class _Result:
            returncode = 0
            stdout = ""
            stderr = ""
        return _Result()

    monkeypatch.setattr(camp_offer_notification_service.subprocess, "run", fake_run)

    response = client.post(
        "/api/v1/recruitment/camp-offers/notify",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "candidate_nos": ["SH1"],
            "choice": "first",
            "template_id": hex_id,
            "simulate": False,
        },
    )

    assert response.status_code == 200, response.text
    cmd = captured["cmd"]
    assert "--offer-md" in cmd
    offer_md_index = cmd.index("--offer-md")
    assert cmd[offer_md_index + 1] == str(target)


def test_camp_offer_stats_returns_headline_counts(
    client: TestClient, monkeypatch
) -> None:
    """The /camp-offers/stats endpoint should surface the four KPI counts
    (sent_mail / agreed / declined / unsigned) plus the total after the
    same filter set as the list endpoint."""
    access_token = _install_principal(
        monkeypatch, "recruiter", ["recruitment_camp_offer:read", "recruitment_camp_offer:write"]
    )

    monkeypatch.setattr(
        "app.api.v1.recruitment.get_camp_offer_stats",
        lambda **kwargs: {
            "sent_mail": 12,
            "agreed": 9,
            "declined": 3,
            "unsigned": 5,
            "total": 24,
        },
    )

    response = client.get(
        "/api/v1/recruitment/camp-offers/stats",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200, response.text
    body = response.json()
    assert body == {
        "sent_mail": 12,
        "agreed": 9,
        "declined": 3,
        "unsigned": 5,
        "total": 24,
    }
