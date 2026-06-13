from __future__ import annotations

import argparse
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
import sys
from pathlib import Path
from typing import Any

from psycopg.rows import dict_row


BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


from app.core.config import settings
from app.services.postgres_state_store import PostgresStateStore


TABLE_NAME = "dtlms_portal_application_personal_statements"


@dataclass(slots=True)
class CandidateComparison:
    candidate_no: str
    primary_rows: list[dict[str, Any]]
    backup_rows: list[dict[str, Any]]

    @property
    def primary_signatures(self) -> list[tuple[Any, ...]]:
        return [row_signature(row) for row in self.primary_rows]

    @property
    def backup_signatures(self) -> list[tuple[Any, ...]]:
        return [row_signature(row) for row in self.backup_rows]

    @property
    def is_matched(self) -> bool:
        return self.primary_signatures == self.backup_signatures

    @property
    def only_primary(self) -> bool:
        return bool(self.primary_rows) and not self.backup_rows

    @property
    def only_backup(self) -> bool:
        return bool(self.backup_rows) and not self.primary_rows

    @property
    def has_diff(self) -> bool:
        return bool(self.primary_rows) and bool(self.backup_rows) and not self.is_matched


@dataclass(slots=True)
class PersonalStatementDiff:
    field_name: str
    primary_value: str
    backup_value: str


@dataclass(slots=True)
class RestoreAction:
    candidate_no: str
    application_id: int
    restore_ai_problem_statement: bool
    restore_ai_industry_opinion: bool
    backup_ai_problem_statement: str
    backup_ai_industry_opinion: str


@dataclass(slots=True)
class RestorePlanSummary:
    action_count: int
    primary_only: int
    backup_only: int
    filled_ai_problem_statement: int
    filled_ai_industry_opinion: int


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Compare dtlms_portal_application_personal_statements between POSTGRES_DB and POSTGRES_BACKUP_DB by candidate_no.",
        epilog="Example: python backend/scripts/compare_portal_application_personal_statements_between_dbs.py --summary",
    )
    parser.add_argument(
        "--primary-database",
        default=settings.postgres_db,
        help=f"Primary database name. Defaults to POSTGRES_DB: {settings.postgres_db}",
    )
    parser.add_argument(
        "--backup-database",
        default=getattr(settings, "postgres_backup_db", ""),
        help=f"Backup database name. Defaults to POSTGRES_BACKUP_DB: {getattr(settings, 'postgres_backup_db', '')}",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Print a short summary after comparison.",
    )
    parser.add_argument(
        "--show-matched",
        action="store_true",
        help="Print rows that match between the two databases.",
    )
    parser.add_argument(
        "--report-file",
        default=str(Path(__file__).resolve().with_suffix(".md")),
        help="Markdown report file path. Defaults to the script name with .md suffix.",
    )
    parser.add_argument(
        "--restore",
        action="store_true",
        help="Restore empty AI fields in the primary database from the backup database.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show restore actions without writing to the primary database.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually write restore actions to the primary database.",
    )
    return parser


def normalize_text(value: Any) -> str:
    return str(value or "").strip()


def format_value(value: Any) -> str:
    text = str(value or "").strip()
    return text if text else "(empty)"


def load_rows(store: PostgresStateStore, database_name: str) -> list[dict[str, Any]]:
    with store._connect(database_name) as conn:
        conn.row_factory = dict_row
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    psm.application_id,
                    ra.candidate_no,
                    ra.student_name,
                    psm.ai_problem_statement,
                    psm.ai_industry_opinion,
                    psm.created_at,
                    psm.updated_at
                FROM dtlms_portal_application_personal_statements AS psm
                JOIN dtlms_recruitment_applications AS ra
                  ON ra.id = psm.application_id
                 AND ra.is_deleted = FALSE
                WHERE COALESCE(BTRIM(ra.candidate_no), '') <> ''
                ORDER BY ra.candidate_no ASC, psm.application_id ASC
                """
            )
            return [dict(row) for row in cur.fetchall()]


def row_signature(row: dict[str, Any]) -> tuple[Any, ...]:
    return (
        normalize_text(row.get("ai_problem_statement")),
        normalize_text(row.get("ai_industry_opinion")),
    )


def row_diff_items(primary_row: dict[str, Any], backup_row: dict[str, Any]) -> list[PersonalStatementDiff]:
    fields = [
        "ai_problem_statement",
        "ai_industry_opinion",
    ]
    diffs: list[PersonalStatementDiff] = []
    for field_name in fields:
        primary_value = normalize_text(primary_row.get(field_name))
        backup_value = normalize_text(backup_row.get(field_name))
        if primary_value != backup_value:
            diffs.append(
                PersonalStatementDiff(
                    field_name=field_name,
                    primary_value=primary_value,
                    backup_value=backup_value,
                )
            )
    return diffs


def build_restore_actions(
    primary_by_candidate: dict[str, list[dict[str, Any]]],
    backup_by_candidate: dict[str, list[dict[str, Any]]],
) -> list[RestoreAction]:
    actions: list[RestoreAction] = []
    for candidate_no in sorted(set(primary_by_candidate) & set(backup_by_candidate)):
        primary_rows = primary_by_candidate.get(candidate_no, [])
        backup_rows = backup_by_candidate.get(candidate_no, [])
        if not primary_rows or not backup_rows:
            continue

        primary_row = primary_rows[0]
        backup_row = backup_rows[0]
        application_id = int(primary_row.get("application_id") or 0)
        if application_id <= 0:
            continue

        restore_ai_problem_statement = not normalize_text(primary_row.get("ai_problem_statement")) and bool(normalize_text(backup_row.get("ai_problem_statement")))
        restore_ai_industry_opinion = not normalize_text(primary_row.get("ai_industry_opinion")) and bool(normalize_text(backup_row.get("ai_industry_opinion")))

        if restore_ai_problem_statement or restore_ai_industry_opinion:
            actions.append(
                RestoreAction(
                    candidate_no=candidate_no,
                    application_id=application_id,
                    restore_ai_problem_statement=restore_ai_problem_statement,
                    restore_ai_industry_opinion=restore_ai_industry_opinion,
                    backup_ai_problem_statement=normalize_text(backup_row.get("ai_problem_statement")),
                    backup_ai_industry_opinion=normalize_text(backup_row.get("ai_industry_opinion")),
                )
            )

    return actions


def print_restore_actions(actions: list[RestoreAction]) -> None:
    if not actions:
        print("[RESTORE] No restore actions planned.")
        return

    print(f"[RESTORE] Planned actions: {len(actions)}")
    for action in actions:
        print(
            f"[RESTORE] candidate_no={action.candidate_no} application_id={action.application_id} "
            f"ai_problem_statement={'yes' if action.restore_ai_problem_statement else 'no'} "
            f"ai_industry_opinion={'yes' if action.restore_ai_industry_opinion else 'no'}"
        )


def build_restore_markdown_report(
    primary_database: str,
    backup_database: str,
    actions: list[RestoreAction],
) -> str:
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    problem_count = sum(1 for action in actions if action.restore_ai_problem_statement)
    opinion_count = sum(1 for action in actions if action.restore_ai_industry_opinion)
    lines: list[str] = [
        "# dtlms_portal_application_personal_statements 恢复计划报表",
        "",
        f"- 生成时间：{generated_at}",
        f"- 主库：{primary_database}",
        f"- 备库：{backup_database}",
        f"- 恢复动作数：{len(actions)}", 
        f"- 将填充 ai_problem_statement 的 candidate_no 数：{problem_count}",
        f"- 将填充 ai_industry_opinion 的 candidate_no 数：{opinion_count}",
        "",
        "## 恢复明细",
        "",
    ]

    if not actions:
        lines.extend(["- 无恢复动作", ""])
        return "\n".join(lines)

    for action in actions:
        lines.extend(
            [
                f"### candidate_no = {action.candidate_no}",
                "",
                f"- application_id：{action.application_id}",
                f"- ai_problem_statement：{'恢复' if action.restore_ai_problem_statement else '不恢复'}",
                f"- ai_industry_opinion：{'恢复' if action.restore_ai_industry_opinion else '不恢复'}",
                "",
            ]
        )

    return "\n".join(lines)


def apply_restore_actions(store: PostgresStateStore, database_name: str, actions: list[RestoreAction]) -> RestorePlanSummary:
    if not actions:
        return RestorePlanSummary(0, 0, 0, 0, 0)

    filled_ai_problem_statement = 0
    filled_ai_industry_opinion = 0
    with store._connect(database_name) as conn:
        conn.row_factory = dict_row
        with conn.cursor() as cur:
            for action in actions:
                if action.restore_ai_problem_statement:
                    cur.execute(
                        """
                        UPDATE dtlms_portal_application_personal_statements
                        SET ai_problem_statement = %s,
                            updated_at = CURRENT_TIMESTAMP
                        WHERE application_id = %s
                          AND COALESCE(BTRIM(ai_problem_statement), '') = ''
                        """,
                        (
                            action.backup_ai_problem_statement,
                            action.application_id,
                        ),
                    )
                    if cur.rowcount > 0:
                        filled_ai_problem_statement += 1

                if action.restore_ai_industry_opinion:
                    cur.execute(
                        """
                        UPDATE dtlms_portal_application_personal_statements
                        SET ai_industry_opinion = %s,
                            updated_at = CURRENT_TIMESTAMP
                        WHERE application_id = %s
                          AND COALESCE(BTRIM(ai_industry_opinion), '') = ''
                        """,
                        (
                            action.backup_ai_industry_opinion,
                            action.application_id,
                        ),
                    )
                    if cur.rowcount > 0:
                        filled_ai_industry_opinion += 1

        conn.commit()

    return RestorePlanSummary(
        action_count=len(actions),
        primary_only=0,
        backup_only=0,
        filled_ai_problem_statement=filled_ai_problem_statement,
        filled_ai_industry_opinion=filled_ai_industry_opinion,
    )


def candidate_row_to_markdown(row: dict[str, Any] | None) -> str:
    if row is None:
        return "(missing)"
    ai_problem_statement = normalize_text(row.get("ai_problem_statement"))
    ai_industry_opinion = normalize_text(row.get("ai_industry_opinion"))
    return (
        f"`application_id={format_value(row.get('application_id'))}` "
        f"`ai_problem_statement={'empty' if not ai_problem_statement else 'filled'}` "
        f"`ai_industry_opinion={'empty' if not ai_industry_opinion else 'filled'}`"
    )


def build_markdown_report(
    primary_database: str,
    backup_database: str,
    comparisons: list[CandidateComparison],
    *,
    only_primary: int,
    only_backup: int,
    matched_same: int,
    matched_diff: int,
    primary_extra_rows: int,
    backup_extra_rows: int,
) -> str:
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines: list[str] = [
        "# dtlms_portal_application_personal_statements 主备库比对报表",
        "",
        f"- 生成时间：{generated_at}",
        f"- 主库：{primary_database}",
        f"- 备库：{backup_database}",
        f"- 比对表：{TABLE_NAME}",
        "",
        "## 汇总",
        "",
        "| 指标 | 数值 |",
        "| --- | ---: |",
        f"| candidate_no 仅在主库存在 | {only_primary} |",
        f"| candidate_no 仅在备库存在 | {only_backup} |",
        f"| candidate_no 在两边完全一致 | {matched_same} |",
        f"| candidate_no 在两边存在差异 | {matched_diff} |",
        f"| 主库多余行数 | {primary_extra_rows} |",
        f"| 备库多余行数 | {backup_extra_rows} |",
        "",
        "## 差异明细",
        "",
    ]

    diff_items = [item for item in comparisons if item.only_primary or item.only_backup or item.has_diff]
    if not diff_items:
        lines.extend(["- 无差异", ""])
        return "\n".join(lines)

    for item in diff_items:
        lines.extend(
            [
                f"### candidate_no = {item.candidate_no}",
                "",
                f"- 主库行数：{len(item.primary_rows)}",
                f"- 备库行数：{len(item.backup_rows)}",
                f"- 主库是否为空：{'是' if not item.primary_rows else '否'}",
                f"- 备库是否为空：{'是' if not item.backup_rows else '否'}",
                "",
                "| 位置 | 主库 | 备库 |",
                "| --- | --- | --- |",
            ]
        )
        max_rows = max(len(item.primary_rows), len(item.backup_rows))
        for index in range(max_rows):
            primary_row = item.primary_rows[index] if index < len(item.primary_rows) else None
            backup_row = item.backup_rows[index] if index < len(item.backup_rows) else None
            lines.append(f"| 第 {index + 1} 行 | {candidate_row_to_markdown(primary_row)} | {candidate_row_to_markdown(backup_row)} |")

        if item.has_diff and item.primary_rows and item.backup_rows:
            primary_row = item.primary_rows[0]
            backup_row = item.backup_rows[0]
            diffs = row_diff_items(primary_row, backup_row)
            if diffs:
                lines.extend(["", "- 字段差异："])
                for diff in diffs:
                    lines.append(f"  - `{diff.field_name}`: {'有区别' if diff.primary_value != diff.backup_value else '无区别'}")
        lines.append("")

    return "\n".join(lines)


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if not args.primary_database:
        print("[ERROR] Primary database is empty. Set POSTGRES_DB or pass --primary-database.", file=sys.stderr)
        return 1
    if not args.backup_database:
        print("[ERROR] Backup database is empty. Set POSTGRES_BACKUP_DB or pass --backup-database.", file=sys.stderr)
        return 1

    store = PostgresStateStore()
    original_database = settings.postgres_db

    try:
        if args.restore:
            try:
                primary_rows = load_rows(store, args.primary_database)
            except Exception as exc:
                print(f"[ERROR] Failed to load rows from primary database {args.primary_database}: {exc}", file=sys.stderr)
                return 1

            try:
                backup_rows = load_rows(store, args.backup_database)
            except Exception as exc:
                print(f"[ERROR] Failed to load rows from backup database {args.backup_database}: {exc}", file=sys.stderr)
                return 1

            primary_by_candidate: dict[str, list[dict[str, Any]]] = defaultdict(list)
            backup_by_candidate: dict[str, list[dict[str, Any]]] = defaultdict(list)

            for row in primary_rows:
                candidate_no = normalize_text(row.get("candidate_no"))
                if candidate_no:
                    primary_by_candidate[candidate_no].append(row)

            for row in backup_rows:
                candidate_no = normalize_text(row.get("candidate_no"))
                if candidate_no:
                    backup_by_candidate[candidate_no].append(row)

            restore_actions = build_restore_actions(primary_by_candidate, backup_by_candidate)
            print_restore_actions(restore_actions)

            report_path = Path(args.report_file).expanduser().resolve()
            report_text = build_restore_markdown_report(
                args.primary_database,
                args.backup_database,
                restore_actions,
            )
            report_path.write_text(report_text, encoding="utf-8")
            print(f"[RESTORE] Markdown report written to: {report_path}")

            if args.dry_run or not args.apply:
                if args.dry_run:
                    print("[RESTORE] Dry run completed. No changes were written.")
                else:
                    print("[RESTORE] No changes were written. Re-run with --apply to persist restore actions.")
                return 0

            summary = apply_restore_actions(store, args.primary_database, restore_actions)
            print(f"[RESTORE] Updated ai_problem_statement rows: {summary.filled_ai_problem_statement}")
            print(f"[RESTORE] Updated ai_industry_opinion rows: {summary.filled_ai_industry_opinion}")
            print(f"[RESTORE] Total written rows: {summary.action_count}")
            return 0

        try:
            primary_rows = load_rows(store, args.primary_database)
        except Exception as exc:
            print(f"[ERROR] Failed to load rows from primary database {args.primary_database}: {exc}", file=sys.stderr)
            return 1

        try:
            backup_rows = load_rows(store, args.backup_database)
        except Exception as exc:
            print(f"[ERROR] Failed to load rows from backup database {args.backup_database}: {exc}", file=sys.stderr)
            return 1

        primary_by_candidate: dict[str, list[dict[str, Any]]] = defaultdict(list)
        backup_by_candidate: dict[str, list[dict[str, Any]]] = defaultdict(list)

        for row in primary_rows:
            candidate_no = normalize_text(row.get("candidate_no"))
            if candidate_no:
                primary_by_candidate[candidate_no].append(row)

        for row in backup_rows:
            candidate_no = normalize_text(row.get("candidate_no"))
            if candidate_no:
                backup_by_candidate[candidate_no].append(row)

        all_candidate_nos = sorted(set(primary_by_candidate) | set(backup_by_candidate))
        comparisons: list[CandidateComparison] = []
        only_primary = 0
        only_backup = 0
        matched_same = 0
        matched_diff = 0
        primary_extra_rows = 0
        backup_extra_rows = 0

        for candidate_no in all_candidate_nos:
            comparison = CandidateComparison(
                candidate_no=candidate_no,
                primary_rows=primary_by_candidate.get(candidate_no, []),
                backup_rows=backup_by_candidate.get(candidate_no, []),
            )
            comparisons.append(comparison)

            if comparison.only_primary:
                only_primary += 1
                primary_extra_rows += len(comparison.primary_rows)
                if args.show_matched:
                    print(f"[ONLY-PRIMARY] candidate_no={candidate_no} primary_rows={len(comparison.primary_rows)}")
                continue

            if comparison.only_backup:
                only_backup += 1
                backup_extra_rows += len(comparison.backup_rows)
                if args.show_matched:
                    print(f"[ONLY-BACKUP] candidate_no={candidate_no} backup_rows={len(comparison.backup_rows)}")
                continue

            if comparison.is_matched:
                matched_same += 1
                if args.show_matched:
                    print(f"[MATCH] candidate_no={candidate_no} rows={len(comparison.primary_rows)}")
                continue

            matched_diff += 1
            primary_extra_rows += max(len(comparison.primary_rows) - len(comparison.backup_rows), 0)
            backup_extra_rows += max(len(comparison.backup_rows) - len(comparison.primary_rows), 0)

            max_rows = max(len(comparison.primary_rows), len(comparison.backup_rows))
            print(f"[DIFF] candidate_no={candidate_no} primary_rows={len(comparison.primary_rows)} backup_rows={len(comparison.backup_rows)}")
            for index in range(max_rows):
                primary_row = comparison.primary_rows[index] if index < len(comparison.primary_rows) else None
                backup_row = comparison.backup_rows[index] if index < len(comparison.backup_rows) else None
                primary_sig = row_signature(primary_row) if primary_row else None
                backup_sig = row_signature(backup_row) if backup_row else None
                if primary_sig == backup_sig:
                    if args.show_matched:
                        print(f"  [ROW {index + 1}] matched")
                    continue
                print(f"  [ROW {index + 1}]")
                print(f"    primary: {candidate_row_to_markdown(primary_row)}")
                print(f"    backup:  {candidate_row_to_markdown(backup_row)}")

        print(f"[INFO] Primary database: {args.primary_database}")
        print(f"[INFO] Backup database: {args.backup_database}")
        print(f"[INFO] Candidate numbers compared: {len(all_candidate_nos)}")

        if args.summary:
            print("[SUMMARY]")
            print(f"- only_primary_candidate_no={only_primary}")
            print(f"- only_backup_candidate_no={only_backup}")
            print(f"- matched_same_candidate_no={matched_same}")
            print(f"- matched_diff_candidate_no={matched_diff}")
            print(f"- primary_extra_rows={primary_extra_rows}")
            print(f"- backup_extra_rows={backup_extra_rows}")

        report_path = Path(args.report_file).expanduser().resolve()
        report_text = build_markdown_report(
            args.primary_database,
            args.backup_database,
            comparisons,
            only_primary=only_primary,
            only_backup=only_backup,
            matched_same=matched_same,
            matched_diff=matched_diff,
            primary_extra_rows=primary_extra_rows,
            backup_extra_rows=backup_extra_rows,
        )
        report_path.write_text(report_text, encoding="utf-8")
        print(f"[INFO] Markdown report written to: {report_path}")

        return 0
    finally:
        settings.postgres_db = original_database


if __name__ == "__main__":
    raise SystemExit(main())
