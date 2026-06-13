from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

from psycopg.rows import dict_row


BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


from app.core.config import settings
from app.services.postgres_state_store import PostgresStateStore


TABLE_NAME = "dtlms_portal_application_english_proficiencies"


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
    def certificate_mismatch(self) -> bool:
        if len(self.primary_rows) != len(self.backup_rows):
            return False
        if not self.is_matched:
            return False
        for index in range(len(self.primary_rows)):
            primary_row = self.primary_rows[index]
            backup_row = self.backup_rows[index]
            if normalize_text(primary_row.get("certificate_attachment_url")) != normalize_text(backup_row.get("certificate_attachment_url")):
                return True
        return False

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

    @property
    def has_certificate_mismatch(self) -> bool:
        if len(self.primary_rows) != len(self.backup_rows):
            return False
        if not self.is_matched:
            return False
        for index in range(len(self.primary_rows)):
            primary_row = self.primary_rows[index]
            backup_row = self.backup_rows[index]
            if normalize_text(primary_row.get("certificate_attachment_url")) != normalize_text(backup_row.get("certificate_attachment_url")):
                return True
        return False


@dataclass(slots=True)
class RestoreAction:
    candidate_no: str
    application_id: int
    source_english_proficiency_id: int
    target_english_proficiency_id: int | None
    exam_name: str
    score_text: str
    certificate_attachment_url: str
    restore_score_text: bool
    restore_certificate_attachment_url: bool
    action_type: str


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Compare dtlms_portal_application_english_proficiencies between POSTGRES_DB and POSTGRES_BACKUP_DB by candidate_no.",
        epilog="Example: python backend/scripts/compare_portal_application_english_proficiencies_between_dbs.py --summary",
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
        help="Restore the primary database from the backup database for matching candidate_no rows.",
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


def load_rows(store: PostgresStateStore, database_name: str) -> list[dict[str, Any]]:
    with store._connect(database_name) as conn:
        conn.row_factory = dict_row
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    ep.application_id,
                    ra.candidate_no,
                    ra.student_name,
                    ep.id AS english_proficiency_id,
                    ep.exam_name,
                    ep.score_text,
                    ep.certificate_attachment_url,
                    ep.created_at,
                    ep.updated_at
                FROM dtlms_portal_application_english_proficiencies AS ep
                JOIN dtlms_recruitment_applications AS ra
                  ON ra.id = ep.application_id
                 AND ra.is_deleted = FALSE
                WHERE COALESCE(BTRIM(ra.candidate_no), '') <> ''
                ORDER BY ra.candidate_no ASC, ep.application_id ASC, ep.id ASC
                """
            )
            return [dict(row) for row in cur.fetchall()]


def row_signature(row: dict[str, Any]) -> tuple[Any, ...]:
    return (
        normalize_text(row.get("exam_name")),
        normalize_text(row.get("score_text")),
    )


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

        application_id = int(primary_rows[0].get("application_id") or 0)
        if application_id <= 0:
            continue

        primary_by_exam = {
            normalize_text(row.get("exam_name")): row
            for row in primary_rows
            if normalize_text(row.get("exam_name"))
        }

        for backup_row in backup_rows:
            exam_name = normalize_text(backup_row.get("exam_name"))
            if not exam_name:
                continue

            primary_row = primary_by_exam.get(exam_name)
            backup_score_text = normalize_text(backup_row.get("score_text"))
            backup_certificate_url = normalize_text(backup_row.get("certificate_attachment_url"))

            if primary_row is None:
                backup_row_id = int(backup_row.get("english_proficiency_id") or 0)
                if backup_row_id <= 0:
                    continue
                actions.append(
                    RestoreAction(
                        candidate_no=candidate_no,
                        application_id=application_id,
                        source_english_proficiency_id=backup_row_id,
                        target_english_proficiency_id=None,
                        exam_name=exam_name,
                        score_text=backup_score_text,
                        certificate_attachment_url=backup_certificate_url,
                        restore_score_text=True,
                        restore_certificate_attachment_url=True,
                        action_type="insert",
                    )
                )
                continue

            primary_row_id = int(primary_row.get("english_proficiency_id") or 0)
            if primary_row_id <= 0:
                continue

            restore_score_text = not normalize_text(primary_row.get("score_text")) and bool(backup_score_text)
            restore_certificate_attachment_url = not normalize_text(primary_row.get("certificate_attachment_url")) and bool(backup_certificate_url)

            if restore_score_text or restore_certificate_attachment_url:
                actions.append(
                    RestoreAction(
                        candidate_no=candidate_no,
                        application_id=application_id,
                        source_english_proficiency_id=int(backup_row.get("english_proficiency_id") or 0),
                        target_english_proficiency_id=primary_row_id,
                        exam_name=exam_name,
                        score_text=backup_score_text,
                        certificate_attachment_url=backup_certificate_url,
                        restore_score_text=restore_score_text,
                        restore_certificate_attachment_url=restore_certificate_attachment_url,
                        action_type="update",
                    )
                )

    return actions


def print_restore_actions(actions: list[RestoreAction]) -> None:
    if not actions:
        print("[RESTORE] No restore actions planned.")
        return
    print(f"[RESTORE] Planned actions: {len(actions)}")
    for action in actions:
        if action.action_type == "insert":
            print(
                f"[RESTORE][INSERT] candidate_no={action.candidate_no} application_id={action.application_id} "
                f"exam_name={action.exam_name} source_english_id={action.source_english_proficiency_id}"
            )
            continue
        print(
            f"[RESTORE][UPDATE] candidate_no={action.candidate_no} application_id={action.application_id} "
            f"target_english_id={action.target_english_proficiency_id} exam_name={action.exam_name} "
            f"score_text={'yes' if action.restore_score_text else 'no'} "
            f"certificate_attachment_url={'yes' if action.restore_certificate_attachment_url else 'no'}"
        )


def build_restore_markdown_report(
    primary_database: str,
    backup_database: str,
    restore_actions: list[RestoreAction],
) -> str:
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    insert_actions = [action for action in restore_actions if action.action_type == "insert"]
    update_actions = [action for action in restore_actions if action.action_type == "update"]
    lines: list[str] = [
        "# dtlms_portal_application_english_proficiencies 恢复计划报表",
        "",
        f"- 生成时间：{generated_at}",
        f"- 主库：{primary_database}",
        f"- 备库：{backup_database}",
        f"- 恢复动作总数：{len(restore_actions)}",
        f"- 插入动作数：{len(insert_actions)}",
        f"- 更新动作数：{len(update_actions)}",
        "",
        "## 恢复明细",
        "",
    ]

    if not restore_actions:
        lines.extend(["- 无恢复动作", ""])
        return "\n".join(lines)

    for action in restore_actions:
        lines.extend(
            [
                f"### candidate_no = {action.candidate_no}",
                "",
                f"- 恢复类型：{'新增缺失行' if action.action_type == 'insert' else '补空值'}",
                f"- application_id：{action.application_id}",
                f"- exam_name：{action.exam_name}",
                f"- score_text：{'恢复' if action.restore_score_text else '不恢复'}",
                f"- certificate_attachment_url：{'恢复' if action.restore_certificate_attachment_url else '不恢复'}",
                f"- 来源 english_proficiency_id：{action.source_english_proficiency_id}",
                f"- 目标 english_proficiency_id：{action.target_english_proficiency_id if action.target_english_proficiency_id is not None else '(insert)'}",
                "",
            ]
        )

    return "\n".join(lines)


def apply_restore_actions(store: PostgresStateStore, primary_database: str, actions: list[RestoreAction]) -> int:
    if not actions:
        return 0

    updated_count = 0
    inserted_count = 0
    with store._connect(primary_database) as conn:
        conn.row_factory = dict_row
        with conn.cursor() as cur:
            for action in actions:
                if action.action_type == "insert":
                    cur.execute(
                        """
                        INSERT INTO dtlms_portal_application_english_proficiencies (
                            application_id,
                            exam_name,
                            score_text,
                            certificate_attachment_url
                        ) VALUES (%s, %s, %s, %s)
                        """,
                        (
                            action.application_id,
                            action.exam_name,
                            action.score_text,
                            action.certificate_attachment_url,
                        ),
                    )
                    if cur.rowcount > 0:
                        inserted_count += 1
                    continue

                if action.target_english_proficiency_id is None:
                    continue

                set_clauses: list[str] = []
                parameters: list[Any] = []
                if action.restore_score_text:
                    set_clauses.append("score_text = %s")
                    parameters.append(action.score_text)
                if action.restore_certificate_attachment_url:
                    set_clauses.append("certificate_attachment_url = %s")
                    parameters.append(action.certificate_attachment_url)
                if not set_clauses:
                    continue

                set_clauses.append("updated_at = CURRENT_TIMESTAMP")
                parameters.append(action.target_english_proficiency_id)
                cur.execute(
                    f"""
                    UPDATE dtlms_portal_application_english_proficiencies
                    SET {', '.join(set_clauses)}
                    WHERE id = %s
                    """,
                    parameters,
                )
                if cur.rowcount > 0:
                    updated_count += 1

        conn.commit()

    print(f"[RESTORE] Updated rows: {updated_count}")
    print(f"[RESTORE] Inserted rows: {inserted_count}")
    return updated_count + inserted_count


def format_value(value: Any) -> str:
    text = str(value or "").strip()
    return text if text else "(empty)"


def candidate_row_to_markdown(row: dict[str, Any] | None) -> str:
    if row is None:
        return "(missing)"
    return (
        f"`id={format_value(row.get('english_proficiency_id'))}` "
        f"`application_id={format_value(row.get('application_id'))}` "
        f"`exam_name={format_value(row.get('exam_name'))}` "
        f"`score_text={format_value(row.get('score_text'))}` "
        f"`certificate_attachment_url={format_value(row.get('certificate_attachment_url'))}`"
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
    certificate_mismatch: int,
    primary_extra_rows: int,
    backup_extra_rows: int,
) -> str:
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines: list[str] = [
        "# dtlms_portal_application_english_proficiencies 主备库比对报表",
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
        f"| 仅附件 URL 不一致的 candidate_no | {certificate_mismatch} |",
        f"| 主库多余行数 | {primary_extra_rows} |",
        f"| 备库多余行数 | {backup_extra_rows} |",
        "",
        "## 差异明细",
        "",
    ]

    diff_items = [item for item in comparisons if item.only_primary or item.only_backup or item.has_diff or item.has_certificate_mismatch]
    if not diff_items:
        lines.extend(["- 无差异", ""])
    else:
        for item in diff_items:
            lines.extend(
                [
                    f"### candidate_no = {item.candidate_no}",
                    "",
                    f"- 主库行数：{len(item.primary_rows)}",
                    f"- 备库行数：{len(item.backup_rows)}",
                    f"- 附件 URL 是否一致：{'否' if item.has_certificate_mismatch else '是'}",
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
            if item.has_certificate_mismatch:
                lines.extend(
                    [
                        "",
                        "> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。",
                    ]
                )
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

            restored_count = apply_restore_actions(store, args.primary_database, restore_actions)
            print(f"[RESTORE] Total written rows: {restored_count}")
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
        certificate_mismatch = 0
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
                if comparison.has_certificate_mismatch:
                    certificate_mismatch += 1
                if args.show_matched:
                    suffix = " certificate_url_diff" if comparison.has_certificate_mismatch else ""
                    print(f"[MATCH] candidate_no={candidate_no} rows={len(comparison.primary_rows)}{suffix}")
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
                print(f"    primary: {(primary_row.get('english_proficiency_id'), primary_row.get('application_id'), primary_row.get('exam_name'), primary_row.get('score_text'), primary_row.get('certificate_attachment_url')) if primary_row else '(missing)'}")
                print(f"    backup:  {(backup_row.get('english_proficiency_id'), backup_row.get('application_id'), backup_row.get('exam_name'), backup_row.get('score_text'), backup_row.get('certificate_attachment_url')) if backup_row else '(missing)'}")

        print(f"[INFO] Primary database: {args.primary_database}")
        print(f"[INFO] Backup database: {args.backup_database}")
        print(f"[INFO] Candidate numbers compared: {len(all_candidate_nos)}")

        if args.summary:
            print("[SUMMARY]")
            print(f"- only_primary_candidate_no={only_primary}")
            print(f"- only_backup_candidate_no={only_backup}")
            print(f"- matched_same_candidate_no={matched_same}")
            print(f"- matched_diff_candidate_no={matched_diff}")
            print(f"- certificate_mismatch_candidate_no={certificate_mismatch}")
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
            certificate_mismatch=certificate_mismatch,
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