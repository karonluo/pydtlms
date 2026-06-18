"""Markdown rendering helpers for camp offer templates.

Reuses the dependency-free renderer inside
``backend.scripts.send_summer_camp_offer_emails`` so the API can preview
uploaded offer.md / offer2.md templates without duplicating parser logic.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


_BACKEND_DIR = Path(__file__).resolve().parents[2]
if str(_BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(_BACKEND_DIR))

_SCRIPT_PATH = (
    Path(__file__).resolve().parents[2] / "scripts" / "send_summer_camp_offer_emails.py"
)


def _load_renderer():
    """Import :func:``render_markdown_to_html`` from the standalone CLI script
    without requiring the ``backend`` package to be on ``sys.path``."""

    spec = importlib.util.spec_from_file_location(
        "send_summer_camp_offer_emails", str(_SCRIPT_PATH)
    )
    if spec is None or spec.loader is None:
        raise ImportError(
            f"无法加载邮件发送脚本: {_SCRIPT_PATH}"
        )
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.render_markdown_to_html


_render_markdown_to_html = _load_renderer()


def render_markdown_to_html(markdown_text: str) -> str:
    """Render an offer-mail Markdown template to a self-contained HTML body."""

    return _render_markdown_to_html(markdown_text)


def render_markdown_file_to_html(path: Path) -> str:
    """Read a Markdown file from disk and render it to HTML."""

    text = Path(path).read_text(encoding="utf-8")
    return render_markdown_to_html(text)


# Placeholder values used by the preview endpoint. These are intentionally
# illustrative only - the real send flow still uses the candidate's actual
# data.
PREVIEW_PLACEHOLDER_VALUES: dict[str, str] = {
    "candidate_no": "SH20270001",
    "student_name": "张三",
    "first_choice": "计算机科学与技术",
    "second_choice": "人工智能",
}


def render_with_sample_placeholders(markdown_text: str) -> str:
    """Render a template after substituting ``{key}`` placeholders with
    illustrative sample data, so reviewers can preview the layout without
    touching the database."""

    rendered = markdown_text
    for key, value in PREVIEW_PLACEHOLDER_VALUES.items():
        rendered = rendered.replace("{" + key + "}", value)
    return render_markdown_to_html(rendered)
