"""Send camp-offer notification emails by delegating to the legacy script.

This module wraps `backend.scripts.send_summer_camp_offer_emails` so the
HTTP API can reuse its existing SMTP / Markdown rendering logic. The script
is invoked as a subprocess with a temporary `--result-json` file, and the
per-candidate results are parsed back into a typed response.
"""

from __future__ import annotations

import json
import logging
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from app.schemas.recruitment import (
    CampOfferNotificationSendResponse,
    CampOfferNotificationSendResultItem,
)

logger = logging.getLogger(__name__)


BACKEND_DIR = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = BACKEND_DIR / "scripts"
OFFER_SCRIPT_PATH = SCRIPTS_DIR / "send_summer_camp_offer_emails.py"

PROJECT_ROOT = BACKEND_DIR.parent
OFFER_TEMPLATE_UPLOAD_DIR = (
    PROJECT_ROOT / "frontend" / "public" / "recruitment" / "offer-templates"
)
OFFER_TEMPLATE_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def _resolve_python_executable() -> str:
    """Pick the Python interpreter used to run the script."""

    override = os.environ.get("DTMLS_PYTHON_EXECUTABLE")
    if override:
        return override
    return sys.executable or "python"


def _builtin_template_path(choice: str) -> Path:
    if choice == "second":
        return SCRIPTS_DIR / "offer2.md"
    return SCRIPTS_DIR / "offer.md"


def _resolve_uploaded_template_path(template_id: str | int) -> Path:
    return OFFER_TEMPLATE_UPLOAD_DIR / f"offer-{template_id}.md"


def _resolve_template_path(
    template_id: str | int | None, choice: str
) -> Path:
    """Resolve a template id to a concrete file path.

    Accepts:

    * `None` / empty -> fall back to the builtin first/second template.
    * `"first"` / `"second"` -> corresponding builtin.
    * alphanumeric id (e.g. the hex id used by uploaded templates) -> ``<upload_dir>/offer-{id}.md``.
    """

    if template_id is None or template_id == "":
        return _builtin_template_path(choice)
    if isinstance(template_id, str):
        key = template_id.strip().lower()
        if key in {"first", "second"}:
            return _builtin_template_path(key)
        if not key:
            raise RuntimeError(f"非法的邮件模板 id: {template_id!r}")
        return _resolve_uploaded_template_path(key)
    if isinstance(template_id, int) and not isinstance(template_id, bool):
        return _resolve_uploaded_template_path(template_id)
    raise RuntimeError(f"非法的邮件模板 id: {template_id!r}")


def send_camp_offer_notifications(
    *,
    candidate_nos: list[str],
    choice: str,
    simulate: bool,
    simulate_recipient: str | None,
    template_id: str | int | None = None,
) -> CampOfferNotificationSendResponse:
    if not OFFER_SCRIPT_PATH.exists():
        raise RuntimeError(f"找不到邮件发送脚本: {OFFER_SCRIPT_PATH}")

    template_path = _resolve_template_path(template_id, choice)
    if not template_path.exists():
        raise RuntimeError(f"找不到指定的邮件模板: {template_path}")

    # When the resolved template is the script default for `choice` we can
    # let the script pick it; otherwise pass an explicit `--offer-md`.
    builtin_default = _builtin_template_path(choice)
    use_offer_md = template_path != builtin_default

    with tempfile.TemporaryDirectory(prefix="dtlms-offer-mail-") as tmpdir:
        result_path = Path(tmpdir) / "result.json"
        cmd: list[str] = [
            _resolve_python_executable(),
            str(OFFER_SCRIPT_PATH),
            "--candidate-no",
            ",".join(candidate_nos),
            "--sent-mail",
            "yes",
            "--choice",
            choice,
            "--result-json",
            str(result_path),
        ]
        if use_offer_md:
            cmd.extend(["--offer-md", str(template_path)])
        if simulate and simulate_recipient:
            cmd.extend(["--simulate-recipient", simulate_recipient])

        logger.info("启动邮件发送脚本: %s", " ".join(cmd))
        try:
            completed = subprocess.run(
                cmd,
                cwd=str(BACKEND_DIR),
                capture_output=True,
                text=True,
                check=False,
            )
        except Exception as exc:
            logger.exception("邮件发送脚本启动失败: %s", exc)
            raise RuntimeError(f"邮件发送脚本启动失败: {exc}") from exc

        if completed.stdout:
            logger.info("邮件脚本 stdout: %s", completed.stdout[-2000:])
        if completed.stderr:
            logger.info("邮件脚本 stderr: %s", completed.stderr[-2000:])

        payload: dict = {}
        if result_path.exists():
            try:
                payload = json.loads(result_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                logger.error("解析邮件结果 JSON 失败: %s", exc)

        results: list[CampOfferNotificationSendResultItem] = []
        for item in payload.get("results", []) or []:
            try:
                results.append(
                    CampOfferNotificationSendResultItem(
                        candidate_no=str(item.get("candidate_no") or ""),
                        email=str(item.get("email") or ""),
                        status=str(item.get("status") or "failed"),
                        error=str(item.get("error") or ""),
                    )
                )
            except Exception:
                continue

        success_count = int(payload.get("success_count", 0) or 0)
        failure_count = int(payload.get("failure_count", 0) or 0)
        if not results and completed.returncode != 0:
            failure_count = len(candidate_nos)
            for no in candidate_nos:
                results.append(
                    CampOfferNotificationSendResultItem(
                        candidate_no=no,
                        email="",
                        status="failed",
                        error=completed.stderr.strip()[:500] or f"exit_code={completed.returncode}",
                    )
                )
            success_count = 0

        message = (
            f"成功 {success_count} 条，失败 {failure_count} 条。"
            if results
            else "邮件发送完成，但脚本未返回逐条结果。"
        )
        return CampOfferNotificationSendResponse(
            message=message,
            choice=choice,
            simulate=simulate,
            simulate_recipient=simulate_recipient if simulate else None,
            template_path=str(template_path),
            success_count=success_count,
            failure_count=failure_count,
            results=results,
        )
