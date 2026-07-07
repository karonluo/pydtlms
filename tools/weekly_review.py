# -*- coding: utf-8 -*-
"""Weekly review draft generator for the pydtlms repository.

Usage (run inside PowerShell at repo root, or pass --repo):

    python tools\\weekly_review.py                # draft the previous week to stdout
    python tools\\weekly_review.py --save         # append into documents\周报\
    python tools\\weekly_review.py --days 3       # last N days (debug)
    python tools\\weekly_review.py --week 2026-W27  # specify ISO week (debug)

Dependencies: Python 3.10+ stdlib only. Repo root must be a git repo.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
WEEKLY_DIR = REPO_ROOT / "documents" / "周报"


def run_git(args):
    proc = subprocess.run(
        ["git", "-C", str(REPO_ROOT), *args],
        capture_output=True, text=True, encoding="utf-8", errors="replace", check=False,
    )
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr)
    return proc.stdout


def collect_since(since, until):
    fmt = "%Y-%m-%dT%H:%M:%S"
    out = run_git([
        "log",
        f"--since={since.strftime(fmt)}",
        f"--until={until.strftime(fmt)}",
        "--no-merges",
        "--pretty=format:===START===%n%H%n%an%n%ad%n%s%n===END===",
        "--date=iso",
    ])
    chunks = out.split("===START===")
    commits = []
    for chunk in chunks[1:]:
        body = chunk.split("===END===", 1)[0]
        lines = [line for line in body.splitlines() if line.strip()]
        if len(lines) < 4:
            continue
        sha, author, date, subject = lines[0], lines[1], lines[2], lines[3]
        subject = subject.strip().strip("`").strip()
        commits.append({"sha": sha, "author": author, "date": date, "subject": subject})
    return commits


def categorize(subject):
    s = subject.lower()
    if s.startswith("feat"):
        return "功能"
    if s.startswith("fix"):
        return "修复"
    if s.startswith("refactor"):
        return "重构"
    if s.startswith("docs") or s.startswith("doc"):
        return "文档"
    if s.startswith("test"):
        return "测试"
    if s.startswith("chore") or s.startswith("build") or s.startswith("ci"):
        return "工程"
    return "其它"


CONVENTIONAL_RE = re.compile(
    r"^(?P<type>feat|fix|refactor|docs|doc|test|chore|build|ci|perf|style)(?:\((?P<scope>[^)]+)\))?:\s*(?P<desc>.+)$"
)


def parse_subject(subject):
    m = CONVENTIONAL_RE.match(subject.strip())
    if not m:
        return ("其它", "", subject.strip())
    return (m.group("type"), m.group("scope") or "", m.group("desc").strip())


def _decode_git_path(raw):
    raw = raw.strip()
    if raw.startswith('"') and raw.endswith('"'):
        raw = raw[1:-1]
    try:
        if "\\" in raw and all(c in "01234567" for c in raw.replace("\\\\", "").replace("\\", "")):
            decoded = b""
            i = 0
            while i < len(raw):
                if raw[i] == "\\" and i + 3 < len(raw) and raw[i + 1] in "01234567":
                    decoded += bytes([int(raw[i + 1:i + 4], 8)])
                    i += 4
                else:
                    decoded += raw[i].encode("utf-8")
                    i += 1
            return decoded.decode("utf-8", errors="replace")
    except Exception:
        pass
    return raw


def diff_stat(since, until):
    fmt = "%Y-%m-%dT%H:%M:%S"
    out = run_git([
        "-c", "core.quotePath=false",
        "log",
        f"--since={since.strftime(fmt)}",
        f"--until={until.strftime(fmt)}",
        "--no-merges",
        "--pretty=tformat:",
        "--numstat",
    ])
    files = add = delete = 0
    dir_counter = {}
    for line in out.splitlines():
        line = line.rstrip()
        if not line.strip():
            continue
        parts = line.split("\t", 2)
        if len(parts) != 3:
            parts = line.split(None, 2)
        if len(parts) != 3:
            continue
        a, d, path = parts
        try:
            ai, di = int(a), int(d)
        except ValueError:
            continue
        path = _decode_git_path(path)
        if not path:
            continue
        files += 1
        add += ai
        delete += di
        top = path.split("/", 1)[0] if "/" in path else path
        dir_counter[top] = dir_counter.get(top, 0) + 1
    top_dirs = sorted(dir_counter.items(), key=lambda kv: kv[1], reverse=True)[:5]
    return files, add, delete, top_dirs


def bulletize(commits):
    if not commits:
        return "- （本周无提交）"
    buckets = {}
    for c in commits:
        buckets.setdefault(categorize(c["subject"]), []).append(c)
    order = ["功能", "修复", "重构", "文档", "测试", "工程", "其它"]
    lines = []
    for cat in order:
        items = buckets.get(cat)
        if not items:
            continue
        lines.append(f"### {cat}（{len(items)}）")
        for c in items:
            t, scope, desc = parse_subject(c["subject"])
            short = c["sha"][:7]
            scope_part = f"`{scope}` " if scope else ""
            lines.append(f"- {scope_part}{desc}（{short}）")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="起草 pydtlms 周报")
    parser.add_argument("--days", type=int, default=7, help="回看天数（默认 7）")
    parser.add_argument("--save", action="store_true", help="追加写入 documents/周报/")
    parser.add_argument("--repo", default=str(REPO_ROOT), help="仓库根目录")
    parser.add_argument("--week", default=None, help="指定 ISO 周，格式 2026-W27")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    if not (repo / ".git").exists():
        sys.stderr.write(f"错误：{repo} 不是 git 仓库\n")
        return 1

    today = dt.date.today()
    if args.week:
        try:
            year_str, week_str = args.week.split("-W")
            week_start = dt.date.fromisocalendar(int(year_str), int(week_str), 1)
        except ValueError:
            sys.stderr.write("错误：--week 必须是 2026-W27 这样的格式\n")
            return 2
        week_end_date = week_start + dt.timedelta(days=7)
    else:
        week_start = today - dt.timedelta(days=today.weekday() + args.days)
        week_end_date = today

    since = dt.datetime.combine(week_start, dt.time.min)
    until = dt.datetime.combine(week_end_date, dt.time.min)

    commits = collect_since(since, until)
    files, add, delete, top_dirs = diff_stat(since, until)

    title_week = week_start.isocalendar()
    header = f"# 周报 {week_start.isoformat()} - {(week_end_date - dt.timedelta(days=1)).isoformat()}（第 {title_week.week} 周）"
    summary_lines = [
        header,
        "",
        "> 由 `tools/weekly_review.py` 起草。提交明细基于 `git log`，请人工润色后再发。",
        "",
        "## 本周概览",
        f"- 提交数：**{len(commits)}**",
        f"- 变更文件：**{files}**（新增 {add} 行 / 删除 {delete} 行）",
        "- 重点目录（按文件数）：" + ("、".join(f"`{d}`x{n}" for d, n in top_dirs) if top_dirs else "（无）"),
        "",
        "## 工作明细",
        bulletize(commits),
        "",
        "## 待办 / 下周计划",
        "- （请人工补充）",
        "",
        "## 备注 / 风险",
        "- （请人工补充）",
        "",
    ]
    text = "\n".join(summary_lines)

    if args.save:
        WEEKLY_DIR.mkdir(parents=True, exist_ok=True)
        out_path = WEEKLY_DIR / f"周报_{week_start.isoformat()}_W{title_week.week:02d}.md"
        out_path.write_text(text, encoding="utf-8")
        print(f"已写入：{out_path}")
    else:
        sys.stdout.write(text)
        sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())