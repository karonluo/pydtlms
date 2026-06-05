from __future__ import annotations

from datetime import datetime
import json
import logging
from pathlib import Path
from typing import Any, TYPE_CHECKING, cast

import psycopg
from psycopg.rows import dict_row

from app.core.config import BACKEND_DIR, settings


logger = logging.getLogger(__name__)


class PostgresStateStoreQueryMixin:
    if TYPE_CHECKING:
        def ensure_schema(self) -> None: ...

        def _connect(self, database_name: str, autocommit: bool = False) -> psycopg.Connection[Any]: ...

        def __getattr__(self, name: str) -> Any: ...

    @staticmethod
    def _resolve_attachment_name(
        attachment_rows: list[dict[str, Any]],
        owner_type: str,
        owner_id: int | None,
        category: str,
        fallback_url: str | None = None,
    ) -> str | None:
        for item in attachment_rows:
            if str(item.get("owner_type") or "") != owner_type:
                continue
            if str(item.get("attachment_category") or "") != category:
                continue
            current_owner_id = item.get("owner_id")
            if owner_id is not None and int(current_owner_id or 0) != int(owner_id):
                continue
            file_name = str(item.get("file_name") or "").strip()
            if file_name:
                return file_name
        if fallback_url:
            return Path(str(fallback_url)).name or None
        return None

    @staticmethod
    def _execute_dynamic(
        cur: psycopg.Cursor[Any],
        query: str,
        params: Any | None = None,
    ) -> None:
        cur.execute(cast(Any, query), params)

    @staticmethod
    def _require_row(row: Any, context: str) -> dict[str, Any]:
        if row is None:
            raise RuntimeError(f"Expected row for {context}")
        return dict(cast(dict[str, Any], row))

    @staticmethod
    def _require_scalar_row(row: Any, context: str) -> Any:
        if row is None:
            raise RuntimeError(f"Expected row for {context}")
        return row

    @staticmethod
    def _principal_field_value(principal: Any | None, field_name: str) -> Any:
        if principal is None:
            return None
        if isinstance(principal, dict):
            return principal.get(field_name)
        return getattr(principal, field_name, None)

    @classmethod
    def _principal_role_codes(cls, principal: Any | None) -> set[str]:
        raw_roles = cls._principal_field_value(principal, "roles") or []
        return {str(item).strip() for item in raw_roles if str(item).strip()}

    @classmethod
    def _needs_center_scope_filter(cls, principal: Any | None) -> bool:
        role_codes = cls._principal_role_codes(principal)
        if not role_codes:
            return False
        if role_codes.intersection({"platform_admin", "AILABMGT", "academy_admin"}):
            return False
        return "advisor" in role_codes

    def get_system_user_by_id(self, user_id: int) -> dict[str, Any] | None:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        u.id,
                        u.username,
                        u.full_name,
                        u.password_hash,
                        COALESCE(r.role_code, '') AS role_code,
                        COALESCE(r.role_name, '') AS role_name,
                        COALESCE(up.department_name, u.department_name, '') AS department_name,
                        up.introduction AS introduction,
                        COALESCE(up.email, u.email) AS email,
                        COALESCE(up.phone_number, u.phone_number) AS phone_number,
                        CASE WHEN u.is_active THEN '启用' ELSE '停用' END AS account_status,
                        u.last_login_at
                    FROM dtlms_users u
                    LEFT JOIN dtlms_user_roles ur ON ur.user_id = u.id
                    LEFT JOIN dtlms_roles r ON r.id = ur.role_id AND r.is_deleted = FALSE
                    LEFT JOIN dtlms_user_profiles up ON up.username = u.username
                    WHERE u.id = %s AND u.is_deleted = FALSE
                    LIMIT 1
                    """,
                    (int(user_id),),
                )
                row = cur.fetchone()
                if row is None:
                    return None
                normalized = self._normalize_system_user_row(dict(row))
                normalized["password_hash"] = row.get("password_hash")
                return normalized

    def get_system_user_by_username(self, username: str) -> dict[str, Any] | None:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        u.id,
                        u.username,
                        u.full_name,
                        u.password_hash,
                        COALESCE(r.role_code, '') AS role_code,
                        COALESCE(r.role_name, '') AS role_name,
                        COALESCE(up.department_name, u.department_name, '') AS department_name,
                        up.introduction AS introduction,
                        COALESCE(up.email, u.email) AS email,
                        COALESCE(up.phone_number, u.phone_number) AS phone_number,
                        CASE WHEN u.is_active THEN '启用' ELSE '停用' END AS account_status,
                        u.last_login_at,
                        COALESCE(array_agg(DISTINCT p.permission_code) FILTER (WHERE p.permission_code IS NOT NULL), ARRAY[]::varchar[]) AS permissions
                    FROM dtlms_users u
                    LEFT JOIN dtlms_user_roles ur ON ur.user_id = u.id
                    LEFT JOIN dtlms_roles r ON r.id = ur.role_id AND r.is_deleted = FALSE
                    LEFT JOIN dtlms_role_permissions rp ON rp.role_id = r.id
                    LEFT JOIN dtlms_permissions p ON p.id = rp.permission_id AND p.is_deleted = FALSE
                    LEFT JOIN dtlms_user_profiles up ON up.username = u.username
                    WHERE u.username = %s AND u.is_deleted = FALSE
                    GROUP BY u.id, u.username, u.full_name, u.password_hash, r.role_code, r.role_name, up.department_name, u.department_name, up.introduction, up.email, u.email, up.phone_number, u.phone_number, u.is_active, u.last_login_at
                    LIMIT 1
                    """,
                    (str(username),),
                )
                row = cur.fetchone()
                if row is None:
                    return None
                normalized = self._normalize_system_user_row(dict(row))
                normalized["password_hash"] = row.get("password_hash")
                normalized["permissions"] = [str(item) for item in (row.get("permissions") or []) if str(item).strip()]
                return normalized

    def system_username_exists(self, username: str, *, exclude_user_id: int | None = None) -> bool:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            with conn.cursor() as cur:
                if exclude_user_id is None:
                    cur.execute(
                        "SELECT 1 FROM dtlms_users WHERE username = %s AND is_deleted = FALSE LIMIT 1",
                        (str(username),),
                    )
                else:
                    cur.execute(
                        "SELECT 1 FROM dtlms_users WHERE username = %s AND is_deleted = FALSE AND id <> %s LIMIT 1",
                        (str(username), int(exclude_user_id)),
                    )
                return cur.fetchone() is not None

    def load_role_state(self) -> list[dict[str, Any]]:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        r.id,
                        r.role_code,
                        r.role_name,
                        COALESCE(r.scope_name, '系统管理') AS scope_name,
                        COALESCE(array_agg(DISTINCT p.permission_code) FILTER (WHERE p.permission_code IS NOT NULL), ARRAY[]::varchar[]) AS permissions,
                        COUNT(DISTINCT ur.user_id) FILTER (WHERE u.is_deleted = FALSE) AS user_count
                    FROM dtlms_roles r
                    LEFT JOIN dtlms_role_permissions rp ON rp.role_id = r.id
                    LEFT JOIN dtlms_permissions p ON p.id = rp.permission_id AND p.is_deleted = FALSE
                    LEFT JOIN dtlms_user_roles ur ON ur.role_id = r.id
                    LEFT JOIN dtlms_users u ON u.id = ur.user_id
                    WHERE r.is_deleted = FALSE
                    GROUP BY r.id
                    ORDER BY r.id ASC
                    """
                )
                return [self._normalize_role_row(dict(row)) for row in cur.fetchall()]

    def get_role_by_id(self, role_id: int) -> dict[str, Any] | None:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        r.id,
                        r.role_code,
                        r.role_name,
                        COALESCE(r.scope_name, '系统管理') AS scope_name,
                        COALESCE(array_agg(DISTINCT p.permission_code) FILTER (WHERE p.permission_code IS NOT NULL), ARRAY[]::varchar[]) AS permissions,
                        COUNT(DISTINCT ur.user_id) FILTER (WHERE u.is_deleted = FALSE) AS user_count
                    FROM dtlms_roles r
                    LEFT JOIN dtlms_role_permissions rp ON rp.role_id = r.id
                    LEFT JOIN dtlms_permissions p ON p.id = rp.permission_id AND p.is_deleted = FALSE
                    LEFT JOIN dtlms_user_roles ur ON ur.role_id = r.id
                    LEFT JOIN dtlms_users u ON u.id = ur.user_id
                    WHERE r.id = %s AND r.is_deleted = FALSE
                    GROUP BY r.id
                    LIMIT 1
                    """,
                    (int(role_id),),
                )
                row = cur.fetchone()
                return self._normalize_role_row(dict(row)) if row is not None else None

    def role_code_exists(self, role_code: str, *, exclude_role_id: int | None = None) -> bool:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            with conn.cursor() as cur:
                if exclude_role_id is None:
                    cur.execute(
                        "SELECT 1 FROM dtlms_roles WHERE role_code = %s AND is_deleted = FALSE LIMIT 1",
                        (str(role_code),),
                    )
                else:
                    cur.execute(
                        "SELECT 1 FROM dtlms_roles WHERE role_code = %s AND is_deleted = FALSE AND id <> %s LIMIT 1",
                        (str(role_code), int(exclude_role_id)),
                    )
                return cur.fetchone() is not None

    def missing_permission_codes(self, permission_codes: list[str]) -> list[str]:
        normalized_codes = list(dict.fromkeys(str(code).strip() for code in permission_codes if str(code).strip()))
        if not normalized_codes:
            return []
        placeholders = ", ".join(["%s"] * len(normalized_codes))
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            with conn.cursor() as cur:
                self._execute_dynamic(
                    cur,
                    f"SELECT permission_code FROM dtlms_permissions WHERE is_deleted = FALSE AND permission_code IN ({placeholders})",
                    normalized_codes,
                )
                existing_codes = {str(row[0]).strip() for row in cur.fetchall() if str(row[0]).strip()}
        return [code for code in normalized_codes if code not in existing_codes]

    def load_system_user_state(self) -> list[dict[str, Any]]:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        u.id,
                        u.username,
                        u.full_name,
                        u.password_hash,
                        COALESCE(r.role_code, '') AS role_code,
                        COALESCE(r.role_name, '') AS role_name,
                        COALESCE(up.department_name, u.department_name, '') AS department_name,
                        up.introduction AS introduction,
                        COALESCE(up.email, u.email) AS email,
                        COALESCE(up.phone_number, u.phone_number) AS phone_number,
                        CASE WHEN u.is_active THEN '启用' ELSE '停用' END AS account_status,
                        u.last_login_at
                    FROM dtlms_users u
                    LEFT JOIN dtlms_user_roles ur ON ur.user_id = u.id
                    LEFT JOIN dtlms_roles r ON r.id = ur.role_id AND r.is_deleted = FALSE
                    LEFT JOIN dtlms_user_profiles up ON up.username = u.username
                    WHERE u.is_deleted = FALSE
                    ORDER BY u.id ASC
                    """
                )
                rows: list[dict[str, Any]] = []
                for row in cur.fetchall():
                    normalized = self._normalize_system_user_row(dict(row))
                    normalized["password_hash"] = row.get("password_hash")
                    rows.append(normalized)
                return rows

    def get_role_deletion_preview(self, role_id: int) -> dict[str, Any] | None:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, role_code, role_name, COALESCE(scope_name, '系统管理') AS scope_name
                    FROM dtlms_roles
                    WHERE id = %s AND is_deleted = FALSE
                    LIMIT 1
                    """,
                    (int(role_id),),
                )
                role_row = cur.fetchone()
                if role_row is None:
                    return None
                cur.execute(
                    """
                    SELECT
                        u.id,
                        u.username,
                        u.full_name,
                        role_counts.role_count,
                        fallback.role_code AS fallback_role_code,
                        fallback.role_name AS fallback_role_name
                    FROM dtlms_users u
                    JOIN dtlms_user_roles ur_target ON ur_target.user_id = u.id AND ur_target.role_id = %s
                    LEFT JOIN LATERAL (
                        SELECT COUNT(*) AS role_count
                        FROM dtlms_user_roles ur_all
                        JOIN dtlms_roles r_all ON r_all.id = ur_all.role_id AND r_all.is_deleted = FALSE
                        WHERE ur_all.user_id = u.id
                    ) role_counts ON TRUE
                    LEFT JOIN LATERAL (
                        SELECT r_rem.role_code, r_rem.role_name
                        FROM dtlms_user_roles ur_rem
                        JOIN dtlms_roles r_rem ON r_rem.id = ur_rem.role_id AND r_rem.is_deleted = FALSE
                        WHERE ur_rem.user_id = u.id AND ur_rem.role_id <> %s
                        ORDER BY r_rem.id ASC
                        LIMIT 1
                    ) fallback ON TRUE
                    WHERE u.is_deleted = FALSE
                    ORDER BY u.id ASC
                    """,
                    (int(role_id), int(role_id)),
                )
                assigned_users: list[dict[str, Any]] = []
                blocking_users: list[dict[str, Any]] = []
                for row in cur.fetchall():
                    role_count = int(row.get("role_count") or 0)
                    can_be_unbound = role_count > 1 and bool(row.get("fallback_role_code"))
                    item = {
                        "id": int(row["id"]),
                        "username": str(row["username"]),
                        "full_name": str(row["full_name"]),
                        "role_count": role_count,
                        "fallback_role_code": row.get("fallback_role_code"),
                        "fallback_role_name": row.get("fallback_role_name"),
                        "can_be_unbound": can_be_unbound,
                    }
                    assigned_users.append(item)
                    if not can_be_unbound:
                        blocking_users.append(item)
                return {
                    "id": int(role_row["id"]),
                    "role_code": str(role_row["role_code"]),
                    "role_name": str(role_row["role_name"]),
                    "scope_name": str(role_row["scope_name"]),
                    "assigned_users": assigned_users,
                    "blocking_users": blocking_users,
                    "assigned_user_count": len(assigned_users),
                    "blocking_user_count": len(blocking_users),
                    "can_force_delete": len(blocking_users) == 0,
                    "message": (
                        f"该角色当前被 {len(assigned_users)} 位用户使用。"
                        if assigned_users
                        else "该角色当前未被任何用户使用，可直接删除。"
                    ),
                }

    def load_user_profile_state(self) -> dict[str, dict[str, Any]]:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT username, full_name, role_name, department_name, introduction, phone_number, email, theme_color
                    FROM dtlms_user_profiles
                    ORDER BY username ASC
                    """
                )
                return {str(row["username"]): dict(row) for row in cur.fetchall()}

    def load_audit_policy_state(self) -> list[dict[str, Any]]:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, item, policy, status
                    FROM dtlms_audit_policies
                    WHERE is_deleted = FALSE
                    ORDER BY id ASC
                    """
                )
                return [self._normalize_audit_policy_row(dict(row)) for row in cur.fetchall()]

    def get_audit_policy_by_id(self, policy_id: int) -> dict[str, Any] | None:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, item, policy, status
                    FROM dtlms_audit_policies
                    WHERE id = %s AND is_deleted = FALSE
                    LIMIT 1
                    """,
                    (int(policy_id),),
                )
                row = cur.fetchone()
                return self._normalize_audit_policy_row(dict(row)) if row is not None else None

    def load_integration_state(self) -> list[dict[str, Any]]:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, name, direction, cadence, status, owner
                    FROM dtlms_integrations
                    WHERE is_deleted = FALSE
                    ORDER BY id ASC
                    """
                )
                return [self._normalize_integration_row(dict(row)) for row in cur.fetchall()]

    def get_integration_by_id(self, integration_id: int) -> dict[str, Any] | None:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, name, direction, cadence, status, owner
                    FROM dtlms_integrations
                    WHERE id = %s AND is_deleted = FALSE
                    LIMIT 1
                    """,
                    (int(integration_id),),
                )
                row = cur.fetchone()
                return self._normalize_integration_row(dict(row)) if row is not None else None

    def get_system_stats_snapshot(self) -> dict[str, int]:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        (SELECT COUNT(*) FROM dtlms_integrations WHERE is_deleted = FALSE) AS integration_total,
                        (SELECT COUNT(*) FROM dtlms_integrations WHERE is_deleted = FALSE AND status = '正常') AS active_integration_total,
                        (SELECT COUNT(*) FROM dtlms_operation_logs) AS operation_log_total,
                        (SELECT COUNT(*) FROM dtlms_data_sync_logs WHERE sync_status <> 'success') AS sync_failure_total,
                        (SELECT COUNT(*) FROM dtlms_users WHERE is_deleted = FALSE) AS user_total,
                        (SELECT COUNT(*) FROM dtlms_roles WHERE is_deleted = FALSE) AS role_total
                    """
                )
                row = cur.fetchone()
                return {
                    "integration_total": int(row["integration_total"] if row else 0),
                    "active_integration_total": int(row["active_integration_total"] if row else 0),
                    "operation_log_total": int(row["operation_log_total"] if row else 0),
                    "sync_failure_total": int(row["sync_failure_total"] if row else 0),
                    "user_total": int(row["user_total"] if row else 0),
                    "role_total": int(row["role_total"] if row else 0),
                }

    def get_recruitment_application_detail(self, application_id: int) -> dict[str, Any] | None:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        ra.*,
                        pp.full_name_pinyin,
                        pp.profile_photo_url,
                        pp.id_card_collage_url,
                        pp.gender,
                        pp.birth_date,
                        pp.ethnic_group,
                        pp.native_place,
                        pp.political_status,
                        pp.marital_status,
                        pp.religious_belief,
                        pp.id_type,
                        pp.mailing_address,
                        pp.emergency_contact_name,
                        pp.emergency_contact_phone,
                        rf.field_name AS intended_field,
                        am.material_status,
                        qr.reviewer_username AS reviewer_name,
                        ad.final_score
                    FROM dtlms_recruitment_applications ra
                    LEFT JOIN dtlms_portal_students ps ON ps.id = ra.portal_student_id
                    LEFT JOIN dtlms_portal_student_profiles pp ON pp.portal_student_id = ps.id
                    LEFT JOIN dtlms_research_fields rf ON rf.id = ra.intended_field_id AND rf.is_deleted = FALSE
                    LEFT JOIN LATERAL (
                        SELECT material_status
                        FROM dtlms_application_materials
                        WHERE application_id = ra.id AND is_deleted = FALSE
                        ORDER BY updated_at DESC, id DESC
                        LIMIT 1
                    ) am ON TRUE
                    LEFT JOIN LATERAL (
                        SELECT reviewer_username
                        FROM dtlms_qualification_reviews
                        WHERE application_id = ra.id
                        ORDER BY updated_at DESC, id DESC
                        LIMIT 1
                    ) qr ON TRUE
                    LEFT JOIN LATERAL (
                        SELECT final_score
                        FROM dtlms_admission_decisions
                        WHERE application_id = ra.id
                        ORDER BY updated_at DESC, id DESC
                        LIMIT 1
                    ) ad ON TRUE
                    WHERE ra.id = %s AND ra.is_deleted = FALSE
                    """,
                    (int(application_id),),
                )
                application_row = cur.fetchone()
                if application_row is None:
                    return None

                cur.execute(
                    """
                    SELECT owner_type, owner_id, attachment_category, file_name, file_url
                    FROM dtlms_portal_application_attachments
                    WHERE application_id = %s
                    ORDER BY id ASC
                    """,
                    (int(application_id),),
                )
                attachment_rows = [dict(item) for item in cur.fetchall()]

                cur.execute(
                    """
                    SELECT preference_order, research_center_name, advisor_name, is_optional
                    FROM dtlms_portal_application_preferences
                    WHERE application_id = %s
                    ORDER BY preference_order ASC, id ASC
                    """,
                    (int(application_id),),
                )
                preferences = [dict(item) for item in cur.fetchall()]

                cur.execute(
                    """
                    SELECT id, sort_order, education_stage, start_month, end_month, school_name, major_name,
                           average_score, gpa, ranking, verifier_name, verifier_phone,
                              transcript_attachment_url, degree_certificate_attachment_url, graduation_certificate_attachment_url
                    FROM dtlms_portal_application_education_experiences
                    WHERE application_id = %s
                    ORDER BY sort_order ASC, id ASC
                    """,
                    (int(application_id),),
                )
                education_experiences: list[dict[str, Any]] = []
                for item in cur.fetchall():
                    education = dict(item)
                    education_id = int(education.get("id") or 0)
                    transcript_url = education.get("transcript_attachment_url")
                    degree_url = education.get("degree_certificate_attachment_url")
                    graduation_url = education.get("graduation_certificate_attachment_url")
                    education["transcript_attachment_name"] = self._resolve_attachment_name(
                        attachment_rows, "education_experience", education_id, "transcript", transcript_url
                    )
                    education["degree_certificate_attachment_name"] = self._resolve_attachment_name(
                        attachment_rows, "education_experience", education_id, "degree_certificate", degree_url
                    )
                    education["graduation_certificate_attachment_name"] = self._resolve_attachment_name(
                        attachment_rows, "education_experience", education_id, "graduation_certificate", graduation_url
                    )
                    education.pop("id", None)
                    education_experiences.append(education)

                cur.execute(
                    """
                    SELECT start_month, end_month, organization_name, position_name, responsibility_text,
                           verifier_name, verifier_phone
                    FROM dtlms_portal_application_practice_experiences
                    WHERE application_id = %s
                    ORDER BY id ASC
                    """,
                    (int(application_id),),
                )
                practice_experiences = [dict(item) for item in cur.fetchall()]

                cur.execute(
                    """
                    SELECT id, exam_name, score_text, certificate_attachment_url
                    FROM dtlms_portal_application_english_proficiencies
                    WHERE application_id = %s
                    ORDER BY id ASC
                    """,
                    (int(application_id),),
                )
                english_proficiencies: list[dict[str, Any]] = []
                for item in cur.fetchall():
                    english = dict(item)
                    english_id = int(english.get("id") or 0)
                    english["certificate_attachment_name"] = self._resolve_attachment_name(
                        attachment_rows,
                        "english_proficiency",
                        english_id,
                        "english_certificate",
                        english.get("certificate_attachment_url"),
                    )
                    english.pop("id", None)
                    english_proficiencies.append(english)

                cur.execute(
                    """
                    SELECT member_name, relation_type, employer_name, job_title, contact_phone
                    FROM dtlms_portal_application_family_members
                    WHERE application_id = %s
                    ORDER BY id ASC
                    """,
                    (int(application_id),),
                )
                family_members = [dict(item) for item in cur.fetchall()]

                cur.execute(
                    """
                    SELECT id, achievement_type, paper_title, author_order, journal_or_conference,
                           publish_or_index_month, achievement_month, award_name, award_rank,
                           award_certificate_attachment_url, awarding_organization, award_level,
                           award_year, description_text, responsibility_text
                    FROM dtlms_portal_application_achievement_records
                    WHERE application_id = %s
                    ORDER BY id ASC
                    """,
                    (int(application_id),),
                )
                achievement_records: list[dict[str, Any]] = []
                for item in cur.fetchall():
                    achievement = dict(item)
                    achievement_id = int(achievement.get("id") or 0)
                    achievement["award_certificate_attachment_name"] = self._resolve_attachment_name(
                        attachment_rows,
                        "achievement_record",
                        achievement_id,
                        "achievement_award_certificate",
                        achievement.get("award_certificate_attachment_url"),
                    )
                    achievement.pop("id", None)
                    achievement_records.append(achievement)

                cur.execute(
                    """
                    SELECT
                        personal_statement_text,
                        growth_experience_text,
                        program_application_reason_text,
                        career_plan_text,
                        resume_attachment_url,
                        supporting_material_attachment_url,
                        ai_problem_statement,
                        ai_industry_opinion
                    FROM dtlms_portal_application_personal_statements
                    WHERE application_id = %s
                    """,
                    (int(application_id),),
                )
                personal_statement_row = cur.fetchone()
                personal_statement = dict(personal_statement_row) if personal_statement_row else {}
                personal_statement["resume_attachment_name"] = self._resolve_attachment_name(
                    attachment_rows,
                    "personal_statement",
                    int(application_id),
                    "resume",
                    personal_statement.get("resume_attachment_url") if personal_statement else None,
                )
                personal_statement["supporting_material_attachment_name"] = self._resolve_attachment_name(
                    attachment_rows,
                    "portal_application",
                    int(application_id),
                    "materials",
                    (
                        personal_statement.get("supporting_material_attachment_url")
                        if personal_statement
                        else application_row.get("material_list_attachment")
                    )
                    or application_row.get("material_list_attachment"),
                )
                if personal_statement and not personal_statement.get("supporting_material_attachment_url"):
                    personal_statement["supporting_material_attachment_url"] = application_row.get("material_list_attachment")

                cur.execute(
                    """
                    SELECT has_read_declaration, declaration_text, progress_snapshot
                    FROM dtlms_portal_application_declarations
                    WHERE application_id = %s
                    """,
                    (int(application_id),),
                )
                declaration_row = cur.fetchone()

                cur.execute(
                    """
                    SELECT
                        evaluator_user_id,
                        evaluator_username,
                        evaluator_name,
                        evaluator_role_code,
                        assessment_result,
                        assessment_comment,
                        assessed_at
                    FROM dtlms_background_assessments
                    WHERE application_id = %s
                    ORDER BY assessed_at ASC, id ASC
                    """,
                    (int(application_id),),
                )
                background_assessments = [dict(item) for item in cur.fetchall()]

                cur.execute(
                    """
                    SELECT
                        reviewer_username,
                        reviewer_name,
                        reviewer_role_code,
                        action,
                        action_label,
                        review_comment,
                        reviewed_at
                    FROM dtlms_qualification_review_logs
                    WHERE application_id = %s
                    ORDER BY reviewed_at DESC, id DESC
                    """,
                    (int(application_id),),
                )
                qualification_review_history = [dict(item) for item in cur.fetchall()]

                screening_round = str(application_row.get("advisor_screening_round") or "").strip()
                current_screening_batch_id = (
                    int(application_row.get("second_choice_screening_batch_id") or 0)
                    if screening_round == "second_choice"
                    else int(application_row.get("first_choice_screening_batch_id") or 0)
                ) or None
                if current_screening_batch_id is None:
                    current_screening_batch_id = int(application_row.get("first_choice_screening_batch_id") or 0) or int(application_row.get("second_choice_screening_batch_id") or 0) or None

                advisor_screening_batch: dict[str, Any] = {}
                if current_screening_batch_id is not None:
                    cur.execute(
                        """
                        SELECT signature_base64, submitted_at
                        FROM dtlms_advisor_screening_batches
                        WHERE id = %s
                        LIMIT 1
                        """,
                        (int(current_screening_batch_id),),
                    )
                    advisor_screening_batch_row = cur.fetchone()
                    if advisor_screening_batch_row is not None:
                        advisor_screening_batch = dict(advisor_screening_batch_row)

                application = self._normalize_recruitment_application_row(dict(application_row))
                profile = self._derive_portal_profile(dict(application_row))
                if profile is not None:
                    application["profile"] = profile
                application["background_assessments"] = [
                    {
                        **item,
                        "assessed_at": self._stringify_datetime(item.get("assessed_at")),
                    }
                    for item in background_assessments
                ]
                application["qualification_review_history"] = [
                    {
                        **item,
                        "reviewed_at": self._stringify_datetime(item.get("reviewed_at")),
                    }
                    for item in qualification_review_history
                ]
                application["preferences"] = preferences
                application["education_experiences"] = education_experiences
                application["practice_experiences"] = practice_experiences
                application["english_proficiencies"] = english_proficiencies
                application["family_members"] = family_members
                application["achievement_records"] = achievement_records
                application["personal_statement"] = personal_statement
                application["declaration"] = dict(declaration_row) if declaration_row else {"has_read_declaration": False}
                application["advisor_signature_base64"] = advisor_screening_batch.get("signature_base64")
                application["advisor_screening_submitted_at"] = self._stringify_datetime(
                    advisor_screening_batch.get("submitted_at")
                    or application.get("second_choice_screening_submitted_at")
                    or application.get("first_choice_screening_submitted_at")
                )
                application["material_list_attachment_name"] = self._resolve_attachment_name(
                    attachment_rows,
                    "portal_application",
                    int(application_id),
                    "materials",
                    application.get("material_list_attachment"),
                )
                return application

    def load_team_state(self) -> list[dict[str, Any]]:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        t.id,
                        t.team_code,
                        t.team_name,
                        COALESCE(t.department_name, '') AS department_name,
                        COALESCE(t.discipline_name, '') AS discipline_name,
                        COALESCE(t.lead_user_id, lead.user_id) AS lead_user_id,
                        COALESCE(lead.full_name, '') AS lead_advisor_name,
                        COALESCE(advisor_names.advisor_names, ARRAY[]::text[]) AS advisor_names,
                        COALESCE(advisor_names.advisor_user_ids, ARRAY[]::bigint[]) AS advisor_ids,
                        COALESCE(advisor_names.advisor_relation_ids, ARRAY[]::bigint[]) AS advisor_relation_ids,
                        t.research_directions,
                        t.team_status,
                        COALESCE(TO_CHAR(t.established_on, 'YYYY-MM-DD'), TO_CHAR(t.created_at::date, 'YYYY-MM-DD')) AS established_on,
                        t.description
                    FROM dtlms_teams t
                    LEFT JOIN dtlms_advisors lead ON lead.id = t.lead_advisor_id AND lead.is_deleted = FALSE
                    LEFT JOIN LATERAL (
                        SELECT
                            array_agg(advisor_rows.advisor_name ORDER BY advisor_rows.sort_role, advisor_rows.advisor_name, advisor_rows.relation_id) AS advisor_names,
                            array_agg(advisor_rows.advisor_user_id ORDER BY advisor_rows.sort_role, advisor_rows.advisor_name, advisor_rows.relation_id) AS advisor_user_ids,
                            array_agg(advisor_rows.relation_id ORDER BY advisor_rows.sort_role, advisor_rows.advisor_name, advisor_rows.relation_id) AS advisor_relation_ids
                        FROM (
                            SELECT DISTINCT
                                ta.id AS relation_id,
                                COALESCE(ta.advisor_user_id, advisor.user_id) AS advisor_user_id,
                                advisor.full_name AS advisor_name,
                                CASE WHEN ta.advisor_role = 'lead' THEN 0 ELSE 1 END AS sort_role
                            FROM dtlms_team_advisors ta
                            JOIN dtlms_advisors advisor ON advisor.id = ta.advisor_id AND advisor.is_deleted = FALSE
                            WHERE ta.team_id = t.id AND ta.is_deleted = FALSE
                        ) advisor_rows
                    ) advisor_names ON TRUE
                    WHERE t.is_deleted = FALSE
                    ORDER BY t.id
                    """
                )
                rows = cur.fetchall()

        return [
            {
                "id": int(row["id"]),
                "team_code": row["team_code"],
                "team_name": row["team_name"],
                "department_name": row["department_name"],
                "discipline_name": row["discipline_name"],
                "lead_user_id": int(row.get("lead_user_id") or 0) or None,
                "lead_advisor_name": row["lead_advisor_name"] or None,
                "advisor_names": list(row["advisor_names"] or []),
                "advisor_ids": [int(item) for item in (row.get("advisor_ids") or []) if item is not None],
                "advisor_relation_ids": [int(item) for item in (row.get("advisor_relation_ids") or []) if item is not None],
                "research_directions": self._split_delimited_values(row["research_directions"]),
                "status": self._team_status_label(row["team_status"]),
                "established_on": row["established_on"],
                "description": row["description"],
            }
            for row in rows
        ]

    def load_student_state(self) -> list[dict[str, Any]]:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        s.id,
                        s.portal_student_id,
                        s.student_no,
                        s.full_name,
                        s.current_status,
                        COALESCE(a.full_name, '') AS advisor_name,
                        COALESCE(t.team_name, '') AS team_name,
                        s.degree_type,
                        s.enrollment_year,
                        s.phone_number,
                        s.political_status
                    FROM dtlms_students s
                    LEFT JOIN dtlms_advisors a ON a.id = s.primary_advisor_id AND a.is_deleted = FALSE
                    LEFT JOIN dtlms_teams t ON t.id = s.team_id AND t.is_deleted = FALSE
                    WHERE s.is_deleted = FALSE
                    ORDER BY s.id DESC
                    """
                )
                rows = cur.fetchall()

        return [
            {
                "id": int(row["id"]),
                "portal_student_id": int(row.get("portal_student_id") or 0) or None,
                "student_no": str(row.get("student_no") or ""),
                "full_name": str(row.get("full_name") or ""),
                "status": self._student_status_label(row.get("current_status")),
                "advisor_name": str(row.get("advisor_name") or ""),
                "team_name": str(row.get("team_name") or ""),
                "degree_type": str(row.get("degree_type") or ""),
                "enrollment_year": int(row.get("enrollment_year") or 0),
                "phone_number": row.get("phone_number"),
                "political_status": row.get("political_status"),
            }
            for row in rows
        ]

    def load_recruitment_plan_state(self) -> list[dict[str, Any]]:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        rp.id,
                        rp.plan_name,
                        rp.academic_year,
                        rp.semester,
                        rp.brochure_image_url,
                        rp.plan_description,
                        rp.plan_status,
                        rp.target_quota,
                        COUNT(ra.id) FILTER (WHERE ra.is_deleted = FALSE) AS application_count
                    FROM dtlms_recruitment_plans rp
                    LEFT JOIN dtlms_recruitment_applications ra ON ra.plan_id = rp.id
                    WHERE rp.is_deleted = FALSE
                    GROUP BY rp.id, rp.plan_name, rp.academic_year, rp.semester, rp.brochure_image_url, rp.plan_description, rp.plan_status, rp.target_quota
                    ORDER BY rp.id DESC
                    """
                )
                rows = cur.fetchall()

        results: list[dict[str, Any]] = []
        for row in rows:
            normalized = self._normalize_recruitment_plan_row(dict(row))
            normalized["current_stage"] = str(row.get("plan_status") or "报名配置")
            normalized["target_quota"] = int(row.get("target_quota") or 0)
            normalized["interview_group_count"] = 0
            normalized["is_open"] = True
            results.append(normalized)
        return results

    def load_recruitment_application_state(self) -> list[dict[str, Any]]:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        ra.*, 
                        rf.field_name AS intended_field
                    FROM dtlms_recruitment_applications ra
                    LEFT JOIN dtlms_research_fields rf ON rf.id = ra.intended_field_id
                    WHERE ra.is_deleted = FALSE
                    ORDER BY COALESCE(ra.applied_at, ra.created_at) DESC, ra.id DESC
                    """
                )
                rows = cur.fetchall()
        return [self._normalize_recruitment_application_row(dict(row)) for row in rows]

    def load_portal_student_state(self) -> list[dict[str, Any]]:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        ps.id,
                        ps.full_name,
                        ps.phone_number,
                        ps.email,
                        ps.id_number,
                        ps.account_status,
                        ps.password_hash,
                        ps.gender,
                        ps.birth_date,
                        ps.ethnic_group,
                        ps.native_place,
                        ps.marital_status,
                        ps.religious_belief,
                        ps.id_type,
                        ps.mailing_address,
                        ps.graduation_school,
                        ps.highest_degree,
                        ps.intended_field,
                        ps.political_status,
                        ps.english_level,
                        ps.family_info,
                        ps.education_experience,
                        ps.practice_experience,
                        ps.personal_profile,
                        ps.recommendation_notes,
                        ps.personal_statement_text,
                        ps.signed_agreement,
                        ps.selected_plan_id,
                        ps.selected_team_id,
                        ps.selected_team_name,
                        ps.selected_advisor_user_id,
                        ps.selected_advisor_name,
                        ps.self_evaluation,
                        ps.submitted_at,
                        ps.created_at,
                        ps.updated_at,
                        pp.full_name_pinyin,
                        pp.profile_photo_url,
                        pp.id_card_collage_url,
                        pp.emergency_contact_name,
                        pp.emergency_contact_phone
                    FROM dtlms_portal_students ps
                    LEFT JOIN dtlms_portal_student_profiles pp ON pp.portal_student_id = ps.id
                    ORDER BY ps.id DESC
                    """
                )
                rows = cur.fetchall()

        results: list[dict[str, Any]] = []
        for row in rows:
            student = dict(row)
            profile = self._derive_portal_profile(student)
            if profile is not None:
                student["profile"] = profile
            student.pop("application_draft", None)
            results.append(student)
        return results

    def load_workflow_task_state(self) -> list[dict[str, Any]]:
        # Reuse the PostgreSQL paged workflow query so startup does one batched read
        # instead of replaying a per-task snapshot query for every history row.
        items, _ = self.list_workflow_tasks_page(page=1, page_size=1_000_000)
        return items

    def get_portal_student_detail(self, student_id: int) -> dict[str, Any] | None:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        ps.*,
                        pp.full_name_pinyin,
                        pp.profile_photo_url,
                        pp.id_card_collage_url,
                        pp.emergency_contact_name,
                        pp.emergency_contact_phone
                    FROM dtlms_portal_students ps
                    LEFT JOIN dtlms_portal_student_profiles pp ON pp.portal_student_id = ps.id
                    WHERE ps.id = %s
                    """,
                    (int(student_id),),
                )
                row = cur.fetchone()
                if not row:
                    return None
                student = dict(row)
                saved_draft = dict(student.get("application_draft")) if isinstance(student.get("application_draft"), dict) else None
                profile = self._derive_portal_profile(student)
                if profile is not None:
                    student["profile"] = profile

                selected_plan_id = student.get("selected_plan_id")
                cur.execute(
                    """
                    SELECT id, plan_id, business_key, candidate_no, source_channel, source_channel_other,
                           intended_advisor_name, application_status, applied_at,
                           advisor_screening_status, advisor_screening_round,
                           initial_screening_status, initial_screening_result,
                           first_choice_team_id, second_choice_team_id, intended_advisor_user_id
                    FROM dtlms_recruitment_applications
                    WHERE is_deleted = FALSE AND portal_student_id = %s
                    ORDER BY CASE WHEN plan_id = %s THEN 0 ELSE 1 END,
                             COALESCE(applied_at, created_at) DESC,
                             id DESC
                    LIMIT 1
                    """,
                    (int(student_id), int(selected_plan_id) if selected_plan_id is not None else -1),
                )
                application = cur.fetchone()
                if not application:
                    draft = self._derive_portal_application_draft(student)
                    if draft is not None:
                        student["application_draft"] = draft
                    return student

                application_id = int(application["id"])
                cur.execute(
                    """
                    SELECT preference_order, team_id, research_center_name, advisor_user_id, advisor_name, is_optional
                    FROM dtlms_portal_application_preferences
                    WHERE application_id = %s
                    ORDER BY preference_order ASC, id ASC
                    """,
                    (application_id,),
                )
                preferences = [dict(item) for item in cur.fetchall()]
                cur.execute(
                    """
                    SELECT sort_order, education_stage, start_month, end_month, school_name, major_name,
                           average_score, gpa, ranking, verifier_name, verifier_phone,
                              transcript_attachment_url, degree_certificate_attachment_url, graduation_certificate_attachment_url
                    FROM dtlms_portal_application_education_experiences
                    WHERE application_id = %s
                    ORDER BY sort_order ASC, id ASC
                    """,
                    (application_id,),
                )
                education_experiences = [dict(item) for item in cur.fetchall()]
                cur.execute(
                    """
                    SELECT start_month, end_month, organization_name, position_name, responsibility_text,
                           verifier_name, verifier_phone
                    FROM dtlms_portal_application_practice_experiences
                    WHERE application_id = %s
                    ORDER BY id ASC
                    """,
                    (application_id,),
                )
                practice_experiences = [dict(item) for item in cur.fetchall()]
                cur.execute(
                    """
                    SELECT exam_name, score_text, certificate_attachment_url
                    FROM dtlms_portal_application_english_proficiencies
                    WHERE application_id = %s
                    ORDER BY id ASC
                    """,
                    (application_id,),
                )
                english_proficiencies = [dict(item) for item in cur.fetchall()]
                cur.execute(
                    """
                    SELECT member_name, relation_type, employer_name, job_title, contact_phone
                    FROM dtlms_portal_application_family_members
                    WHERE application_id = %s
                    ORDER BY id ASC
                    """,
                    (application_id,),
                )
                family_members = [dict(item) for item in cur.fetchall()]
                cur.execute(
                    """
                    SELECT id, achievement_type, paper_title, author_order, journal_or_conference,
                           publish_or_index_month, achievement_month, award_name, award_rank,
                           award_certificate_attachment_url, awarding_organization, award_level,
                           award_year, description_text, responsibility_text
                    FROM dtlms_portal_application_achievement_records
                    WHERE application_id = %s
                    ORDER BY id ASC
                    """,
                    (application_id,),
                )
                achievement_rows = [dict(item) for item in cur.fetchall()]
                cur.execute(
                    """
                    SELECT owner_type, owner_id, attachment_category, file_name, file_url
                    FROM dtlms_portal_application_attachments
                    WHERE application_id = %s
                    ORDER BY id ASC
                    """,
                    (application_id,),
                )
                attachment_rows = [dict(item) for item in cur.fetchall()]
                achievement_records = []
                for achievement in achievement_rows:
                    achievement_id = int(achievement.get("id") or 0)
                    achievement["award_certificate_attachment_name"] = self._resolve_attachment_name(
                        attachment_rows,
                        "achievement_record",
                        achievement_id,
                        "achievement_award_certificate",
                        achievement.get("award_certificate_attachment_url"),
                    )
                    achievement.pop("id", None)
                    achievement_records.append(achievement)
                cur.execute(
                    """
                    SELECT
                        personal_statement_text,
                        growth_experience_text,
                        program_application_reason_text,
                        career_plan_text,
                        resume_attachment_url,
                        supporting_material_attachment_url,
                        ai_problem_statement,
                        ai_industry_opinion
                    FROM dtlms_portal_application_personal_statements
                    WHERE application_id = %s
                    """,
                    (application_id,),
                )
                personal_statement_row = cur.fetchone()
                cur.execute(
                    """
                    SELECT has_read_declaration, declaration_text, progress_snapshot
                    FROM dtlms_portal_application_declarations
                    WHERE application_id = %s
                    """,
                    (application_id,),
                )
                declaration_row = cur.fetchone()
                cur.execute(
                    """
                    SELECT
                        evaluator_user_id,
                        evaluator_username,
                        evaluator_name,
                        evaluator_role_code,
                        assessment_result,
                        assessment_comment,
                        assessed_at
                    FROM dtlms_background_assessments
                    WHERE application_id = %s
                    ORDER BY assessed_at ASC, id ASC
                    """,
                    (application_id,),
                )
                background_assessments = [
                    {
                        **dict(item),
                        "assessed_at": self._stringify_datetime(item.get("assessed_at")),
                    }
                    for item in cur.fetchall()
                ]
                student["application_draft"] = {
                    "selected_plan_id": int(application.get("plan_id") or student.get("selected_plan_id") or 0) or None,
                    "selected_team_id": int(student.get("selected_team_id") or 0) or None,
                    "selected_advisor_user_id": int(student.get("selected_advisor_user_id") or 0) or None,
                    "source_channel": application.get("source_channel"),
                    "source_channel_other": application.get("source_channel_other"),
                    "preferences": preferences,
                    "education_experiences": education_experiences,
                    "practice_experiences": practice_experiences,
                    "english_proficiencies": english_proficiencies,
                    "family_members": family_members,
                    "achievement_records": achievement_records,
                    "personal_statement": dict(personal_statement_row) if personal_statement_row else {},
                    "declaration": dict(declaration_row) if declaration_row else {"has_read_declaration": bool(student.get("signed_agreement"))},
                    "submitted_at": None if self._portal_resubmittable_application_status(application.get("application_status")) else self._stringify_datetime(application.get("applied_at")) or student.get("submitted_at"),
                }
                student["application_draft"] = self._merge_portal_application_draft(student.get("application_draft"), saved_draft) or student["application_draft"]
                personal_statement = student["application_draft"]["personal_statement"]
                personal_statement["resume_attachment_name"] = self._resolve_attachment_name(
                    attachment_rows,
                    "personal_statement",
                    application_id,
                    "resume",
                    personal_statement.get("resume_attachment_url"),
                )
                personal_statement["supporting_material_attachment_name"] = self._resolve_attachment_name(
                    attachment_rows,
                    "portal_application",
                    application_id,
                    "materials",
                    personal_statement.get("supporting_material_attachment_url") or application.get("material_list_attachment"),
                )
                if personal_statement and not personal_statement.get("supporting_material_attachment_url"):
                    personal_statement["supporting_material_attachment_url"] = application.get("material_list_attachment")
                student["business_key"] = application.get("business_key")
                student["candidate_no"] = application.get("candidate_no")
                student["recruitment_application_status"] = self._application_status_label(application.get("application_status"))
                student["advisor_screening_status"] = application.get("advisor_screening_status")
                student["advisor_screening_round"] = application.get("advisor_screening_round")
                student["initial_screening_status"] = application.get("initial_screening_status")
                student["initial_screening_result"] = application.get("initial_screening_result")
                student["background_assessments"] = background_assessments
                if preferences:
                    student["selected_team_id"] = int(preferences[0].get("team_id") or application.get("first_choice_team_id") or student.get("selected_team_id") or 0) or None
                    student["selected_team_name"] = preferences[0].get("research_center_name") or student.get("selected_team_name")
                    student["selected_advisor_user_id"] = int(preferences[0].get("advisor_user_id") or application.get("intended_advisor_user_id") or student.get("selected_advisor_user_id") or 0) or None
                    student["selected_advisor_name"] = preferences[0].get("advisor_name") or application.get("intended_advisor_name") or student.get("selected_advisor_name")
                student["selected_plan_id"] = int(application.get("plan_id") or student.get("selected_plan_id") or 0) or None
                student["submitted_at"] = None if self._portal_resubmittable_application_status(application.get("application_status")) else self._stringify_datetime(application.get("applied_at")) or student.get("submitted_at")
                return student

    def list_workflow_tasks_page(
        self,
        status: str | None = None,
        module: str | None = None,
        keyword: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> tuple[list[dict[str, Any]], int]:
        self.ensure_schema()
        offset = max(page - 1, 0) * page_size
        where_clauses = ["1 = 1"]
        params: list[Any] = []

        if status:
            where_clauses.append("COALESCE(vars.task_status, '') = %s")
            params.append(status)
        if module:
            where_clauses.append("COALESCE(vars.business_module, '') = %s")
            params.append(module)
        if keyword and str(keyword).strip():
            where_clauses.append(
                """
                concat_ws(
                    ' ',
                    COALESCE(vars.workflow_name, pd.name_, ''),
                    COALESCE(ht.business_key_, ''),
                    COALESCE(ht.name_, ''),
                    COALESCE(vars.applicant_name, ''),
                    COALESCE(vars.current_handler, '')
                ) ILIKE %s
                """
            )
            params.append(f"%{str(keyword).strip()}%")

        where_sql = " AND ".join(where_clauses)

        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                self._execute_dynamic(
                    cur,
                    f"""
                    SELECT COUNT(*) AS total
                    FROM dtlms_wf_hi_taskinst ht
                    JOIN dtlms_wf_re_procdef pd ON pd.id_ = ht.proc_def_id_
                    LEFT JOIN LATERAL (
                        SELECT
                            MAX(CASE WHEN latest_var.name_ = 'workflowName' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS workflow_name,
                            MAX(CASE WHEN latest_var.name_ = 'businessModule' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS business_module,
                            MAX(CASE WHEN latest_var.name_ = 'applicantName' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS applicant_name,
                            MAX(CASE WHEN latest_var.name_ = 'currentHandler' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS current_handler,
                            MAX(CASE WHEN latest_var.name_ = 'currentNode' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS current_node,
                            MAX(CASE WHEN latest_var.name_ = 'taskStatus' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS task_status,
                            MAX(CASE WHEN latest_var.name_ = 'latestComment' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS latest_comment,
                            MAX(CASE WHEN latest_var.name_ = 'formSummary' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS form_summary
                        FROM (
                            SELECT DISTINCT ON (hv.name_)
                                hv.name_,
                                hv.text_value_,
                                hv.json_value_
                            FROM dtlms_wf_hi_varinst hv
                            WHERE hv.proc_inst_id_ = ht.proc_inst_id_
                            ORDER BY hv.name_, hv.last_updated_time_ DESC, hv.id_ DESC
                        ) latest_var
                    ) vars ON TRUE
                    WHERE {where_sql}
                    """,
                    params,
                )
                total_row = cur.fetchone()
                total = int(total_row["total"] if total_row else 0)

                self._execute_dynamic(
                    cur,
                    f"""
                    SELECT
                        ht.id_ AS task_key,
                        ht.business_key_,
                        ht.name_ AS title,
                        ht.start_time_,
                        ht.due_date_,
                        ht.priority_,
                        ht.proc_def_id_,
                        ht.proc_inst_id_,
                        ht.exec_id_,
                        ht.task_def_key_,
                        pd.key_ AS process_definition_key,
                        pd.name_ AS process_definition_name,
                        vars.workflow_name,
                        vars.business_module,
                        vars.applicant_name,
                        vars.current_handler,
                        vars.current_node,
                        vars.task_status,
                        vars.latest_comment,
                        vars.form_summary,
                        vars.flow_code,
                        vars.node_key,
                        vars.entity_id,
                        vars.candidate_groups,
                        vars.history_entries
                    FROM dtlms_wf_hi_taskinst ht
                    JOIN dtlms_wf_re_procdef pd ON pd.id_ = ht.proc_def_id_
                    LEFT JOIN LATERAL (
                        SELECT
                            MAX(CASE WHEN latest_var.name_ = 'workflowName' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS workflow_name,
                            MAX(CASE WHEN latest_var.name_ = 'businessModule' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS business_module,
                            MAX(CASE WHEN latest_var.name_ = 'applicantName' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS applicant_name,
                            MAX(CASE WHEN latest_var.name_ = 'currentHandler' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS current_handler,
                            MAX(CASE WHEN latest_var.name_ = 'currentNode' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS current_node,
                            MAX(CASE WHEN latest_var.name_ = 'taskStatus' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS task_status,
                            MAX(CASE WHEN latest_var.name_ = 'latestComment' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS latest_comment,
                            MAX(CASE WHEN latest_var.name_ = 'formSummary' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS form_summary,
                            MAX(CASE WHEN latest_var.name_ = 'flowCode' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS flow_code,
                            MAX(CASE WHEN latest_var.name_ = 'nodeKey' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS node_key,
                            MAX(CASE WHEN latest_var.name_ = 'entityId' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS entity_id,
                            MAX(CASE WHEN latest_var.name_ = 'candidateGroups' THEN latest_var.json_value_::text END)::jsonb AS candidate_groups,
                            MAX(CASE WHEN latest_var.name_ = 'historyEntries' THEN latest_var.json_value_::text END)::jsonb AS history_entries
                        FROM (
                            SELECT DISTINCT ON (hv.name_)
                                hv.name_,
                                hv.text_value_,
                                hv.json_value_
                            FROM dtlms_wf_hi_varinst hv
                            WHERE hv.proc_inst_id_ = ht.proc_inst_id_
                            ORDER BY hv.name_, hv.last_updated_time_ DESC, hv.id_ DESC
                        ) latest_var
                    ) vars ON TRUE
                    WHERE {where_sql}
                    ORDER BY ht.start_time_ DESC, ht.id_ DESC
                    LIMIT %s OFFSET %s
                    """,
                    [*params, page_size, offset],
                )
                return [self._normalize_workflow_task_snapshot_row(dict(row)) for row in cur.fetchall()], total

    def list_background_assessments(self, application_id: int) -> list[dict[str, Any]]:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        id,
                        application_id,
                        evaluator_user_id,
                        evaluator_username,
                        evaluator_name,
                        evaluator_role_code,
                        assessment_result,
                        assessment_comment,
                        assessed_at,
                        created_at,
                        updated_at
                    FROM dtlms_background_assessments
                    WHERE application_id = %s
                    ORDER BY assessed_at ASC, id ASC
                    """,
                    (int(application_id),),
                )
                rows = [dict(item) for item in cur.fetchall()]
        return [
            {
                **row,
                "assessed_at": self._stringify_datetime(row.get("assessed_at")),
                "created_at": self._stringify_datetime(row.get("created_at")),
                "updated_at": self._stringify_datetime(row.get("updated_at")),
            }
            for row in rows
        ]

    def get_workflow_task_snapshot(self, task_id: int) -> dict[str, Any] | None:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        ht.id_ AS task_key,
                        ht.business_key_,
                        ht.name_ AS title,
                        ht.start_time_,
                        ht.due_date_,
                        ht.priority_,
                        ht.proc_def_id_,
                        ht.proc_inst_id_,
                        ht.exec_id_,
                        ht.task_def_key_,
                        pd.key_ AS process_definition_key,
                        pd.name_ AS process_definition_name,
                        vars.workflow_name,
                        vars.business_module,
                        vars.applicant_name,
                        vars.current_handler,
                        vars.current_node,
                        vars.task_status,
                        vars.latest_comment,
                        vars.form_summary,
                        vars.flow_code,
                        vars.node_key,
                        vars.entity_id,
                        vars.candidate_groups,
                        vars.history_entries
                    FROM dtlms_wf_hi_taskinst ht
                    JOIN dtlms_wf_re_procdef pd ON pd.id_ = ht.proc_def_id_
                    LEFT JOIN LATERAL (
                        SELECT
                            MAX(CASE WHEN latest_var.name_ = 'workflowName' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS workflow_name,
                            MAX(CASE WHEN latest_var.name_ = 'businessModule' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS business_module,
                            MAX(CASE WHEN latest_var.name_ = 'applicantName' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS applicant_name,
                            MAX(CASE WHEN latest_var.name_ = 'currentHandler' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS current_handler,
                            MAX(CASE WHEN latest_var.name_ = 'currentNode' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS current_node,
                            MAX(CASE WHEN latest_var.name_ = 'taskStatus' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS task_status,
                            MAX(CASE WHEN latest_var.name_ = 'latestComment' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS latest_comment,
                            MAX(CASE WHEN latest_var.name_ = 'formSummary' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS form_summary,
                            MAX(CASE WHEN latest_var.name_ = 'flowCode' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS flow_code,
                            MAX(CASE WHEN latest_var.name_ = 'nodeKey' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS node_key,
                            MAX(CASE WHEN latest_var.name_ = 'entityId' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS entity_id,
                            MAX(CASE WHEN latest_var.name_ = 'candidateGroups' THEN latest_var.json_value_::text END)::jsonb AS candidate_groups,
                            MAX(CASE WHEN latest_var.name_ = 'historyEntries' THEN latest_var.json_value_::text END)::jsonb AS history_entries
                        FROM (
                            SELECT DISTINCT ON (hv.name_)
                                hv.name_,
                                hv.text_value_,
                                hv.json_value_
                            FROM dtlms_wf_hi_varinst hv
                            WHERE hv.proc_inst_id_ = ht.proc_inst_id_
                            ORDER BY hv.name_, hv.last_updated_time_ DESC, hv.id_ DESC
                        ) latest_var
                    ) vars ON TRUE
                    WHERE ht.id_ = %s
                    LIMIT 1
                    """,
                    (f"TASK-{int(task_id)}",),
                )
                row = cur.fetchone()
                return self._normalize_workflow_task_snapshot_row(dict(row)) if row else None

    def list_training_plans_page(
        self,
        keyword: str | None = None,
        plan_status: str | None = None,
        advisor_name: str | None = None,
        report_cycle: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> tuple[list[dict[str, Any]], int]:
        self.ensure_schema()
        offset = max(page - 1, 0) * page_size
        where_clauses = ["tp.is_deleted = FALSE"]
        params: list[Any] = []

        if keyword and str(keyword).strip():
            where_clauses.append(
                """
                CONCAT_WS(
                    ' ',
                    COALESCE(s.student_no, ''),
                    COALESCE(s.full_name, ''),
                    COALESCE(tp.scientific_goal, '')
                ) ILIKE %s
                """
            )
            params.append(f"%{str(keyword).strip()}%")
        if plan_status:
            where_clauses.append("tp.plan_status = %s")
            params.append(self._map_training_plan_status(plan_status))
        if advisor_name:
            where_clauses.append("COALESCE(a.full_name, '') = %s")
            params.append(advisor_name)
        if report_cycle:
            where_clauses.append("COALESCE(tp.report_cycle, '') = %s")
            params.append(report_cycle)

        where_sql = " AND ".join(where_clauses)

        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                self._execute_dynamic(
                    cur,
                    f"""
                    SELECT COUNT(*) AS total
                    FROM dtlms_training_plans tp
                    JOIN dtlms_students s ON s.id = tp.student_id AND s.is_deleted = FALSE
                    JOIN dtlms_advisors a ON a.id = tp.advisor_id AND a.is_deleted = FALSE
                    WHERE {where_sql}
                    """,
                    params,
                )
                total_row = cur.fetchone()
                total = int(total_row["total"] if total_row else 0)

                self._execute_dynamic(
                    cur,
                    f"""
                    SELECT
                        tp.id,
                        s.student_no,
                        s.full_name AS student_name,
                        a.full_name AS advisor_name,
                        tp.version_no,
                        tp.report_cycle,
                        tp.plan_status,
                        tp.scientific_goal,
                        tp.assessment_rule
                    FROM dtlms_training_plans tp
                    JOIN dtlms_students s ON s.id = tp.student_id AND s.is_deleted = FALSE
                    JOIN dtlms_advisors a ON a.id = tp.advisor_id AND a.is_deleted = FALSE
                    WHERE {where_sql}
                    ORDER BY tp.id DESC
                    LIMIT %s OFFSET %s
                    """,
                    [*params, page_size, offset],
                )
                return [self._normalize_training_plan_row(dict(row)) for row in cur.fetchall()], total

    def list_recruitment_plans_page(
        self,
        keyword: str | None = None,
        semester: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> tuple[list[dict[str, Any]], int]:
        self.ensure_schema()
        offset = max(page - 1, 0) * page_size
        where_clauses = ["rp.is_deleted = FALSE"]
        params: list[Any] = []

        if keyword and str(keyword).strip():
            keyword_like = f"%{str(keyword).strip()}%"
            where_clauses.append(
                """
                (
                    rp.plan_name ILIKE %s
                    OR CONCAT_WS(' ', COALESCE(rp.academic_year, ''), COALESCE(rp.semester, '')) ILIKE %s
                    OR COALESCE(rp.plan_description, '') ILIKE %s
                )
                """
            )
            params.extend([keyword_like, keyword_like, keyword_like])
        if semester:
            where_clauses.append("rp.semester = %s")
            params.append(semester)

        where_sql = " AND ".join(where_clauses)

        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                count_sql = f"""
                    SELECT COUNT(*) AS total
                    FROM dtlms_recruitment_plans rp
                    WHERE {where_sql}
                """
                self._execute_dynamic(cur, count_sql, params)
                total_row = cur.fetchone()
                total = int(total_row["total"] if total_row else 0)

                page_sql = f"""
                    SELECT
                        rp.id,
                        rp.plan_name,
                        rp.academic_year,
                        rp.semester,
                        rp.brochure_image_url,
                        rp.plan_description,
                        COUNT(ra.id) FILTER (WHERE ra.is_deleted = FALSE) AS application_count
                    FROM dtlms_recruitment_plans rp
                    LEFT JOIN dtlms_recruitment_applications ra ON ra.plan_id = rp.id
                    WHERE {where_sql}
                    GROUP BY rp.id, rp.plan_name, rp.academic_year, rp.semester, rp.brochure_image_url, rp.plan_description
                    ORDER BY rp.id DESC
                    LIMIT %s OFFSET %s
                """
                self._execute_dynamic(cur, page_sql, [*params, page_size, offset])
                return [self._normalize_recruitment_plan_row(dict(row)) for row in cur.fetchall()], total

    def list_scientific_reports_page(
        self,
        keyword: str | None = None,
        status: str | None = None,
        reviewer_name: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> tuple[list[dict[str, Any]], int]:
        self.ensure_schema()
        offset = max(page - 1, 0) * page_size
        where_clauses = ["sr.is_deleted = FALSE"]
        params: list[Any] = []

        if status:
            where_clauses.append("sr.report_status = %s")
            params.append(self._map_report_status(status))
        if keyword and str(keyword).strip():
            where_clauses.append(
                """
                CONCAT_WS(
                    ' ',
                    COALESCE(sr.business_key, ''),
                    COALESCE(s.student_no, ''),
                    COALESCE(s.full_name, ''),
                    COALESCE(sr.period_label, ''),
                    COALESCE(sr.summary, '')
                ) ILIKE %s
                """
            )
            params.append(f"%{str(keyword).strip()}%")
        if reviewer_name:
            where_clauses.append("COALESCE(reviewer.full_name, '') = %s")
            params.append(reviewer_name)

        where_sql = " AND ".join(where_clauses)

        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                self._execute_dynamic(
                    cur,
                    f"""
                    SELECT COUNT(*) AS total
                    FROM dtlms_scientific_reports sr
                    JOIN dtlms_students s ON s.id = sr.student_id AND s.is_deleted = FALSE
                    LEFT JOIN dtlms_advisors reviewer ON reviewer.id = sr.reviewer_advisor_id AND reviewer.is_deleted = FALSE
                    WHERE {where_sql}
                    """,
                    params,
                )
                total_row = cur.fetchone()
                total = int(total_row["total"] if total_row else 0)

                self._execute_dynamic(
                    cur,
                    f"""
                    SELECT
                        sr.id,
                        sr.business_key,
                        s.student_no,
                        s.full_name AS student_name,
                        sr.period_label,
                        sr.report_status,
                        reviewer.full_name AS reviewer_name,
                        sr.review_score,
                        sr.summary
                    FROM dtlms_scientific_reports sr
                    JOIN dtlms_students s ON s.id = sr.student_id AND s.is_deleted = FALSE
                    LEFT JOIN dtlms_advisors reviewer ON reviewer.id = sr.reviewer_advisor_id AND reviewer.is_deleted = FALSE
                    WHERE {where_sql}
                    ORDER BY sr.id DESC
                    LIMIT %s OFFSET %s
                    """,
                    [*params, page_size, offset],
                )
                return [self._normalize_scientific_report_row(dict(row)) for row in cur.fetchall()], total

    def list_outbound_studies_page(
        self,
        keyword: str | None = None,
        status: str | None = None,
        study_type: str | None = None,
        advisor_name: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> tuple[list[dict[str, Any]], int]:
        self.ensure_schema()
        offset = max(page - 1, 0) * page_size
        where_clauses = ["os.is_deleted = FALSE"]
        params: list[Any] = []

        if status:
            where_clauses.append("os.approval_status = %s")
            params.append(self._map_outbound_status(status))
        if keyword and str(keyword).strip():
            where_clauses.append(
                """
                CONCAT_WS(
                    ' ',
                    COALESCE(os.business_key, ''),
                    COALESCE(s.student_no, ''),
                    COALESCE(s.full_name, ''),
                    COALESCE(os.destination, ''),
                    COALESCE(os.expected_outcome, '')
                ) ILIKE %s
                """
            )
            params.append(f"%{str(keyword).strip()}%")
        if study_type:
            where_clauses.append("COALESCE(os.study_type, '') = %s")
            params.append(study_type)
        if advisor_name:
            where_clauses.append("COALESCE(a.full_name, '') = %s")
            params.append(advisor_name)

        where_sql = " AND ".join(where_clauses)

        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                self._execute_dynamic(
                    cur,
                    f"""
                    SELECT COUNT(*) AS total
                    FROM dtlms_outbound_studies os
                    JOIN dtlms_students s ON s.id = os.student_id AND s.is_deleted = FALSE
                    JOIN dtlms_advisors a ON a.id = os.advisor_id AND a.is_deleted = FALSE
                    WHERE {where_sql}
                    """,
                    params,
                )
                total_row = cur.fetchone()
                total = int(total_row["total"] if total_row else 0)

                self._execute_dynamic(
                    cur,
                    f"""
                    SELECT
                        os.id,
                        os.business_key,
                        s.student_no,
                        s.full_name AS student_name,
                        a.full_name AS advisor_name,
                        os.study_type,
                        os.destination,
                        os.start_date,
                        os.end_date,
                        os.approval_status,
                        os.expected_outcome
                    FROM dtlms_outbound_studies os
                    JOIN dtlms_students s ON s.id = os.student_id AND s.is_deleted = FALSE
                    JOIN dtlms_advisors a ON a.id = os.advisor_id AND a.is_deleted = FALSE
                    WHERE {where_sql}
                    ORDER BY os.start_date DESC, os.id DESC
                    LIMIT %s OFFSET %s
                    """,
                    [*params, page_size, offset],
                )
                return [self._normalize_outbound_study_row(dict(row)) for row in cur.fetchall()], total

    def list_students_page(
        self,
        keyword: str | None = None,
        status: str | None = None,
        advisor_name: str | None = None,
        center_name: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> tuple[list[dict[str, Any]], int]:
        self.ensure_schema()
        offset = max(page - 1, 0) * page_size
        where_clauses = ["s.is_deleted = FALSE"]
        params: list[Any] = []

        if keyword and str(keyword).strip():
            where_clauses.append(
                """
                (
                    s.student_no ILIKE %s
                    OR s.full_name ILIKE %s
                    OR COALESCE(t.team_name, '') ILIKE %s
                )
                """
            )
            keyword_like = f"%{str(keyword).strip()}%"
            params.extend([keyword_like, keyword_like, keyword_like])
        if status:
            where_clauses.append("s.current_status = %s")
            params.append(self._map_student_status(status))
        if advisor_name:
            where_clauses.append("COALESCE(a.full_name, '') = %s")
            params.append(advisor_name)
        if center_name:
            where_clauses.append("COALESCE(t.team_name, '') = %s")
            params.append(center_name)

        where_sql = " AND ".join(where_clauses)

        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                count_sql = f"""
                    SELECT COUNT(*) AS total
                    FROM dtlms_students s
                    LEFT JOIN dtlms_advisors a ON a.id = s.primary_advisor_id
                    LEFT JOIN dtlms_teams t ON t.id = s.team_id
                    WHERE {where_sql}
                """
                self._execute_dynamic(cur, count_sql, params)
                total_row = cur.fetchone()
                total = int(total_row["total"] if total_row else 0)

                page_sql = f"""
                    SELECT
                        s.id,
                        s.student_no,
                        s.full_name,
                        s.current_status,
                        s.primary_advisor_id AS advisor_id,
                        COALESCE(a.full_name, '') AS advisor_name,
                        COALESCE(t.team_name, '') AS team_name,
                        s.degree_type,
                        s.enrollment_year,
                        s.phone_number,
                        s.political_status
                    FROM dtlms_students s
                    LEFT JOIN dtlms_advisors a ON a.id = s.primary_advisor_id
                    LEFT JOIN dtlms_teams t ON t.id = s.team_id
                    WHERE {where_sql}
                    ORDER BY s.id DESC
                    LIMIT %s OFFSET %s
                """
                self._execute_dynamic(cur, page_sql, [*params, page_size, offset])
                return [self._normalize_student_row(dict(row)) for row in cur.fetchall()], total

    def list_registered_portal_students_page(
        self,
        keyword: str | None = None,
        application_form_status: str | None = None,
        recruitment_application_status: str | None = None,
        exclude_background_assessed_username: str | None = None,
        advisor_names: list[str] | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> tuple[list[dict[str, Any]], int]:
        self.ensure_schema()
        offset = max(page - 1, 0) * page_size
        where_clauses = ["1 = 1"]
        params: list[Any] = []

        if keyword and str(keyword).strip():
            keyword_like = f"%{str(keyword).strip()}%"
            where_clauses.append(
                """
                (
                    ps.full_name ILIKE %s
                    OR ps.phone_number ILIKE %s
                    OR ps.email ILIKE %s
                    OR ps.id_number ILIKE %s
                    OR COALESCE(rp.plan_name, '') ILIKE %s
                    OR COALESCE(ps.selected_advisor_name, '') ILIKE %s
                    OR COALESCE(ps.selected_team_name, '') ILIKE %s
                    OR COALESCE(latest_application.candidate_no, '') ILIKE %s
                    OR COALESCE(latest_application.business_key, '') ILIKE %s
                )
                """
            )
            params.extend([keyword_like] * 9)

        normalized_status = str(application_form_status or "").strip()
        if normalized_status == "已填写报名":
            where_clauses.append("COALESCE(latest_application.application_status, '') <> 'returned'")
            where_clauses.append("COALESCE(ps.submitted_at, latest_application.applied_at) IS NOT NULL")
        elif normalized_status == "驳回重填":
            where_clauses.append("COALESCE(latest_application.application_status, '') = 'returned'")
        elif normalized_status == "未填写报名":
            where_clauses.append("COALESCE(latest_application.application_status, '') <> 'returned'")
            where_clauses.append("COALESCE(ps.submitted_at, latest_application.applied_at) IS NULL")

        normalized_recruitment_status = str(recruitment_application_status or "").strip()
        if normalized_recruitment_status:
            candidate_statuses = [normalized_recruitment_status]
            mapped_recruitment_status = self._map_application_status(normalized_recruitment_status)
            if mapped_recruitment_status != normalized_recruitment_status and self._application_status_label(mapped_recruitment_status) == normalized_recruitment_status:
                candidate_statuses.append(mapped_recruitment_status)
            where_clauses.append("COALESCE(latest_application.application_status, '') = ANY(%s)")
            params.append(candidate_statuses)

        normalized_advisor_names = [str(item).strip() for item in (advisor_names or []) if str(item).strip()]
        if normalized_advisor_names:
            where_clauses.append("COALESCE(ps.selected_advisor_name, '') = ANY(%s)")
            params.append(normalized_advisor_names)

        normalized_background_assessed_username = str(exclude_background_assessed_username or "").strip()
        if normalized_background_assessed_username:
            where_clauses.append(
                """
                (
                    COALESCE(latest_application.application_status, '') <> 'background_review'
                    OR NOT EXISTS (
                        SELECT 1
                        FROM dtlms_background_assessments ba
                        WHERE ba.application_id = latest_application.id
                          AND COALESCE(ba.evaluator_username, '') = %s
                    )
                )
                """
            )
            params.append(normalized_background_assessed_username)

        where_sql = " AND ".join(where_clauses)
        latest_application_sql = """
            LEFT JOIN LATERAL (
                SELECT ra.id, ra.business_key, ra.candidate_no, ra.application_status, ra.applied_at
                FROM dtlms_recruitment_applications ra
                WHERE ra.is_deleted = FALSE AND ra.portal_student_id = ps.id
                ORDER BY COALESCE(ra.applied_at, ra.created_at) DESC, ra.id DESC
                LIMIT 1
            ) latest_application ON TRUE
        """

        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                count_sql = f"""
                    SELECT COUNT(*) AS total
                    FROM dtlms_portal_students ps
                    LEFT JOIN dtlms_recruitment_plans rp ON rp.id = ps.selected_plan_id
                    {latest_application_sql}
                    WHERE {where_sql}
                """
                self._execute_dynamic(cur, count_sql, params)
                total_row = cur.fetchone()
                total = int(total_row["total"] if total_row else 0)

                page_sql = f"""
                    SELECT
                        ps.id,
                        ps.full_name,
                        ps.phone_number,
                        ps.email,
                        ps.id_number,
                        ps.account_status,
                        rp.plan_name AS selected_plan_name,
                        ps.selected_team_name,
                        ps.selected_advisor_name,
                        ps.created_at,
                        ps.submitted_at,
                        latest_application.id AS recruitment_application_id,
                        latest_application.candidate_no AS recruitment_application_candidate_no,
                        latest_application.business_key AS recruitment_application_business_key,
                        latest_application.application_status,
                        latest_application.applied_at
                    FROM dtlms_portal_students ps
                    LEFT JOIN dtlms_recruitment_plans rp ON rp.id = ps.selected_plan_id
                    {latest_application_sql}
                    WHERE {where_sql}
                    ORDER BY ps.created_at DESC, ps.id DESC
                    LIMIT %s OFFSET %s
                """
                self._execute_dynamic(cur, page_sql, [*params, page_size, offset])
                return [self._normalize_registered_portal_student_row(dict(row)) for row in cur.fetchall()], total

    def list_dashboard_undergraduate_school_rankings(self, limit: int = 20) -> list[dict[str, Any]]:
        self.ensure_schema()
        normalized_limit = max(int(limit), 1)
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    WITH latest_application AS (
                        SELECT DISTINCT ON (ps.id)
                            ps.id AS portal_student_id,
                            COALESCE(
                                undergraduate_education.school_name,
                                NULLIF(BTRIM(ra.undergraduate_school), '')
                            ) AS school_name
                        FROM dtlms_portal_students ps
                        JOIN dtlms_recruitment_applications ra ON ra.portal_student_id = ps.id AND ra.is_deleted = FALSE
                        LEFT JOIN LATERAL (
                            SELECT NULLIF(BTRIM(ee.school_name), '') AS school_name
                            FROM dtlms_portal_application_education_experiences ee
                            WHERE ee.application_id = ra.id
                              AND ee.education_stage IN ('本科在读', '本科毕业')
                              AND NULLIF(BTRIM(ee.school_name), '') IS NOT NULL
                            ORDER BY ee.sort_order ASC, ee.id ASC
                            LIMIT 1
                        ) undergraduate_education ON TRUE
                        ORDER BY ps.id, COALESCE(ra.applied_at, ra.created_at) DESC, ra.id DESC
                    )
                    SELECT school_name, COUNT(*)::int AS student_count
                    FROM latest_application
                    WHERE school_name IS NOT NULL AND BTRIM(school_name) <> ''
                    GROUP BY school_name
                    ORDER BY student_count DESC, school_name ASC
                    LIMIT %s
                    """,
                    (normalized_limit,),
                )
                return [
                    {
                        "school_name": str(row.get("school_name") or ""),
                        "student_count": int(row.get("student_count") or 0),
                    }
                    for row in cur.fetchall()
                ]

    def list_dashboard_undergraduate_school_group_distribution(self) -> dict[str, Any]:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    WITH target_groups(dict_type, group_name, group_order) AS (
                        VALUES
                            ('system_c9_university', 'C9大学', 1),
                            ('system_211_university', '211大学', 2),
                            ('system_985_university', '985大学', 3)
                    ),
                    dictionary_schools AS (
                        SELECT
                            tg.dict_type,
                            tg.group_name,
                            tg.group_order,
                            NULLIF(BTRIM(d.label), '') AS school_name,
                            d.sort_order
                        FROM target_groups tg
                        JOIN dtlms_dict_types t
                          ON t.dict_type = tg.dict_type
                         AND t.is_deleted = FALSE
                         AND t.status = '启用'
                        JOIN dtlms_dict_data d
                          ON d.dict_type_id = t.id
                         AND d.dict_type = t.dict_type
                         AND d.is_deleted = FALSE
                         AND d.status = '启用'
                        WHERE NULLIF(BTRIM(d.label), '') IS NOT NULL
                    ),
                    latest_application AS (
                        SELECT DISTINCT ON (ps.id)
                            ps.id AS portal_student_id,
                            COALESCE(
                                undergraduate_education.school_name,
                                NULLIF(BTRIM(ra.undergraduate_school), '')
                            ) AS school_name
                        FROM dtlms_portal_students ps
                        JOIN dtlms_recruitment_applications ra ON ra.portal_student_id = ps.id AND ra.is_deleted = FALSE
                        LEFT JOIN LATERAL (
                            SELECT NULLIF(BTRIM(ee.school_name), '') AS school_name
                            FROM dtlms_portal_application_education_experiences ee
                            WHERE ee.application_id = ra.id
                              AND ee.education_stage IN ('本科在读', '本科毕业')
                              AND NULLIF(BTRIM(ee.school_name), '') IS NOT NULL
                            ORDER BY ee.sort_order ASC, ee.id ASC
                            LIMIT 1
                        ) undergraduate_education ON TRUE
                        ORDER BY ps.id, COALESCE(ra.applied_at, ra.created_at) DESC, ra.id DESC
                    ),
                    latest_application_total AS (
                        SELECT COUNT(*)::int AS total_applications
                        FROM latest_application
                        WHERE school_name IS NOT NULL AND BTRIM(school_name) <> ''
                    ),
                    school_counts AS (
                        SELECT school_name, COUNT(*)::int AS student_count
                        FROM latest_application
                        WHERE school_name IS NOT NULL AND BTRIM(school_name) <> ''
                        GROUP BY school_name
                    ),
                    grouped_counts AS (
                        SELECT
                            ds.dict_type,
                            ds.group_name,
                            ds.group_order,
                            ds.school_name,
                            ds.sort_order,
                            COALESCE(SUM(sc.student_count), 0)::int AS student_count
                        FROM dictionary_schools ds
                        LEFT JOIN school_counts sc ON sc.school_name LIKE ds.school_name || '%%'
                        GROUP BY ds.dict_type, ds.group_name, ds.group_order, ds.school_name, ds.sort_order
                    )
                    SELECT
                        gc.dict_type,
                        gc.group_name,
                        gc.school_name,
                        gc.student_count,
                        SUM(gc.student_count) OVER (PARTITION BY gc.dict_type)::int AS group_total,
                        lat.total_applications
                    FROM grouped_counts gc
                    CROSS JOIN latest_application_total lat
                    ORDER BY gc.group_order ASC, gc.student_count DESC, gc.sort_order ASC, gc.school_name ASC
                    """
                )
                group_order = [
                    ("system_c9_university", "C9大学"),
                    ("system_211_university", "211大学"),
                    ("system_985_university", "985大学"),
                ]
                groups: dict[str, dict[str, Any]] = {
                    dict_type: {"group_name": group_name, "dict_type": dict_type, "total": 0, "items": []}
                    for dict_type, group_name in group_order
                }
                total_applications = 0
                for row in cur.fetchall():
                    dict_type = str(row.get("dict_type") or "")
                    if dict_type not in groups:
                        continue
                    group_total = int(row.get("group_total") or 0)
                    student_count = int(row.get("student_count") or 0)
                    total_applications = int(row.get("total_applications") or total_applications or 0)
                    groups[dict_type]["total"] = group_total
                    groups[dict_type]["items"].append(
                        {
                            "school_name": str(row.get("school_name") or ""),
                            "student_count": student_count,
                            "percentage": round(student_count * 100 / group_total, 2) if group_total else 0.0,
                        }
                    )

                return {
                    "total_applications": total_applications,
                    "groups": [groups[dict_type] for dict_type, _group_name in group_order],
                }

    def list_dashboard_undergraduate_school_group_students(
        self,
        *,
        dict_type: str,
        school_name: str | None = None,
        bucket: str | None = None,
    ) -> list[dict[str, Any]]:
        self.ensure_schema()
        normalized_dict_type = str(dict_type or "").strip()
        normalized_school_name = str(school_name or "").strip()
        normalized_bucket = str(bucket or "").strip().lower()
        allowed_dict_types = {"system_c9_university", "system_211_university", "system_985_university"}
        if normalized_dict_type not in allowed_dict_types:
            return []

        if normalized_bucket == "other":
            selected_condition = "school_rank > %s"
            selected_params: list[Any] = [5]
        elif normalized_school_name:
            selected_condition = "school_name = %s"
            selected_params = [normalized_school_name]
        else:
            return []

        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                self._execute_dynamic(
                    cur,
                    f"""
                    WITH dictionary_schools AS (
                        SELECT
                            NULLIF(BTRIM(d.label), '') AS school_name,
                            d.sort_order
                        FROM dtlms_dict_types t
                        JOIN dtlms_dict_data d
                          ON d.dict_type_id = t.id
                         AND d.dict_type = t.dict_type
                         AND d.is_deleted = FALSE
                         AND d.status = '启用'
                        WHERE t.dict_type = %s
                          AND t.is_deleted = FALSE
                          AND t.status = '启用'
                          AND NULLIF(BTRIM(d.label), '') IS NOT NULL
                    ),
                    latest_application AS (
                        SELECT DISTINCT ON (ps.id)
                            ps.id AS portal_student_id,
                            ps.full_name AS student_name,
                            ps.phone_number,
                            ps.email,
                            ps.created_at AS registered_at,
                            ra.id AS recruitment_application_id,
                            ra.candidate_no,
                            COALESCE(
                                undergraduate_education.school_name,
                                NULLIF(BTRIM(ra.undergraduate_school), '')
                            ) AS school_name
                        FROM dtlms_portal_students ps
                        JOIN dtlms_recruitment_applications ra ON ra.portal_student_id = ps.id AND ra.is_deleted = FALSE
                        LEFT JOIN LATERAL (
                            SELECT NULLIF(BTRIM(ee.school_name), '') AS school_name
                            FROM dtlms_portal_application_education_experiences ee
                            WHERE ee.application_id = ra.id
                              AND ee.education_stage IN ('本科在读', '本科毕业')
                              AND NULLIF(BTRIM(ee.school_name), '') IS NOT NULL
                            ORDER BY ee.sort_order ASC, ee.id ASC
                            LIMIT 1
                        ) undergraduate_education ON TRUE
                        ORDER BY ps.id, COALESCE(ra.applied_at, ra.created_at) DESC, ra.id DESC
                    ),
                    school_counts AS (
                        SELECT
                            ds.school_name,
                            ds.sort_order,
                            COUNT(la.portal_student_id)::int AS student_count
                        FROM dictionary_schools ds
                        LEFT JOIN latest_application la ON la.school_name LIKE ds.school_name || '%%'
                        GROUP BY ds.school_name, ds.sort_order
                    ),
                    ranked_schools AS (
                        SELECT
                            school_name,
                            ROW_NUMBER() OVER (ORDER BY student_count DESC, sort_order ASC, school_name ASC)::int AS school_rank
                        FROM school_counts
                        WHERE student_count > 0
                    ),
                    selected_schools AS (
                        SELECT school_name
                        FROM ranked_schools
                        WHERE {selected_condition}
                    )
                    SELECT
                        la.recruitment_application_id,
                        la.student_name,
                        la.school_name,
                        la.candidate_no,
                        la.registered_at,
                        la.phone_number,
                        la.email
                    FROM latest_application la
                    JOIN selected_schools ss ON la.school_name LIKE ss.school_name || '%%'
                    ORDER BY la.registered_at DESC NULLS LAST, la.recruitment_application_id DESC
                    """,
                    [normalized_dict_type, *selected_params],
                )
                return [
                    {
                        "recruitment_application_id": int(row.get("recruitment_application_id") or 0),
                        "student_name": str(row.get("student_name") or ""),
                        "school_name": row.get("school_name"),
                        "candidate_no": row.get("candidate_no"),
                        "registered_at": self._stringify_datetime(row.get("registered_at")),
                        "phone_number": row.get("phone_number"),
                        "email": row.get("email"),
                    }
                    for row in cur.fetchall()
                    if int(row.get("recruitment_application_id") or 0) > 0
                ]

    def list_dashboard_undergraduate_school_students(self, school_name: str) -> list[dict[str, Any]]:
        self.ensure_schema()
        normalized_school_name = str(school_name or "").strip()
        if not normalized_school_name:
            return []

        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    WITH latest_application AS (
                        SELECT DISTINCT ON (ps.id)
                            ps.id AS portal_student_id,
                            ps.full_name AS student_name,
                            ps.phone_number,
                            ps.email,
                            ps.created_at AS registered_at,
                            ra.id AS recruitment_application_id,
                            ra.candidate_no,
                            COALESCE(
                                undergraduate_education.school_name,
                                NULLIF(BTRIM(ra.undergraduate_school), '')
                            ) AS school_name
                        FROM dtlms_portal_students ps
                        JOIN dtlms_recruitment_applications ra ON ra.portal_student_id = ps.id AND ra.is_deleted = FALSE
                        LEFT JOIN LATERAL (
                            SELECT NULLIF(BTRIM(ee.school_name), '') AS school_name
                            FROM dtlms_portal_application_education_experiences ee
                            WHERE ee.application_id = ra.id
                              AND ee.education_stage IN ('本科在读', '本科毕业')
                              AND NULLIF(BTRIM(ee.school_name), '') IS NOT NULL
                            ORDER BY ee.sort_order ASC, ee.id ASC
                            LIMIT 1
                        ) undergraduate_education ON TRUE
                        ORDER BY ps.id, COALESCE(ra.applied_at, ra.created_at) DESC, ra.id DESC
                    )
                    SELECT recruitment_application_id, student_name, school_name, candidate_no, registered_at, phone_number, email
                    FROM latest_application
                    WHERE school_name LIKE %s
                    ORDER BY registered_at DESC NULLS LAST, recruitment_application_id DESC
                    """,
                    (f"{normalized_school_name}%",),
                )
                return [
                    {
                        "recruitment_application_id": int(row.get("recruitment_application_id") or 0),
                        "student_name": str(row.get("student_name") or ""),
                        "school_name": row.get("school_name"),
                        "candidate_no": row.get("candidate_no"),
                        "registered_at": self._stringify_datetime(row.get("registered_at")),
                        "phone_number": row.get("phone_number"),
                        "email": row.get("email"),
                    }
                    for row in cur.fetchall()
                    if int(row.get("recruitment_application_id") or 0) > 0
                ]

    def list_dashboard_recruitment_advisor_choice_distribution(self) -> dict[str, Any]:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    WITH latest_application AS (
                        SELECT DISTINCT ON (ps.id)
                            ps.id AS portal_student_id,
                            ra.id AS recruitment_application_id,
                            NULLIF(BTRIM(ps.selected_advisor_name), '') AS selected_advisor_name,
                            NULLIF(BTRIM(ra.intended_advisor_name), '') AS intended_advisor_name
                        FROM dtlms_portal_students ps
                        JOIN dtlms_recruitment_applications ra ON ra.portal_student_id = ps.id AND ra.is_deleted = FALSE
                        ORDER BY ps.id, COALESCE(ra.applied_at, ra.created_at) DESC, ra.id DESC
                    ),
                    choice_rows AS (
                        SELECT
                            'first_choice' AS choice_round,
                            COALESCE(
                                NULLIF(BTRIM(pref1.advisor_name), ''),
                                latest_application.selected_advisor_name,
                                latest_application.intended_advisor_name
                            ) AS advisor_name
                        FROM latest_application
                        LEFT JOIN LATERAL (
                            SELECT NULLIF(BTRIM(pref.advisor_name), '') AS advisor_name
                            FROM dtlms_portal_application_preferences pref
                            WHERE pref.application_id = latest_application.recruitment_application_id
                              AND pref.preference_order = 1
                            LIMIT 1
                        ) pref1 ON TRUE
                        UNION ALL
                        SELECT
                            'second_choice' AS choice_round,
                            NULLIF(BTRIM(pref2.advisor_name), '') AS advisor_name
                        FROM latest_application
                        LEFT JOIN LATERAL (
                            SELECT NULLIF(BTRIM(pref.advisor_name), '') AS advisor_name
                            FROM dtlms_portal_application_preferences pref
                            WHERE pref.application_id = latest_application.recruitment_application_id
                              AND pref.preference_order = 2
                            LIMIT 1
                        ) pref2 ON TRUE
                    ),
                    choice_counts AS (
                        SELECT choice_round, advisor_name, COUNT(*)::int AS student_count
                        FROM choice_rows
                        WHERE advisor_name IS NOT NULL AND BTRIM(advisor_name) <> ''
                        GROUP BY choice_round, advisor_name
                    ),
                    ranked_counts AS (
                        SELECT
                            choice_round,
                            advisor_name,
                            student_count,
                            ROW_NUMBER() OVER (PARTITION BY choice_round ORDER BY student_count DESC, advisor_name ASC)::int AS advisor_rank,
                            SUM(student_count) OVER (PARTITION BY choice_round)::int AS total
                        FROM choice_counts
                    ),
                    bucketed_counts AS (
                        SELECT
                            choice_round,
                            CASE WHEN advisor_rank <= 10 THEN advisor_name ELSE '其他导师' END AS advisor_name,
                            CASE WHEN advisor_rank <= 10 THEN advisor_rank ELSE 11 END AS bucket_order,
                            SUM(student_count)::int AS student_count,
                            MAX(total)::int AS total
                        FROM ranked_counts
                        GROUP BY choice_round, CASE WHEN advisor_rank <= 10 THEN advisor_name ELSE '其他导师' END, CASE WHEN advisor_rank <= 10 THEN advisor_rank ELSE 11 END
                    )
                    SELECT
                        choice_round,
                        CASE choice_round
                            WHEN 'first_choice' THEN '第一志愿导师'
                            WHEN 'second_choice' THEN '第二志愿导师'
                            ELSE choice_round
                        END AS choice_name,
                        total,
                        advisor_name,
                        student_count,
                        ROUND(student_count * 100.0 / NULLIF(total, 0), 2)::float AS percentage,
                        bucket_order
                    FROM bucketed_counts
                    ORDER BY CASE choice_round WHEN 'first_choice' THEN 1 WHEN 'second_choice' THEN 2 ELSE 3 END, bucket_order ASC, advisor_name ASC
                    """
                )
                choices: dict[str, dict[str, Any]] = {
                    "first_choice": {"choice_round": "first_choice", "choice_name": "第一志愿导师", "total": 0, "items": []},
                    "second_choice": {"choice_round": "second_choice", "choice_name": "第二志愿导师", "total": 0, "items": []},
                }
                for row in cur.fetchall():
                    choice_round = str(row.get("choice_round") or "")
                    if choice_round not in choices:
                        continue
                    total = int(row.get("total") or 0)
                    student_count = int(row.get("student_count") or 0)
                    choices[choice_round]["total"] = total
                    choices[choice_round]["items"].append(
                        {
                            "advisor_name": str(row.get("advisor_name") or ""),
                            "student_count": student_count,
                            "percentage": float(row.get("percentage") or 0),
                        }
                    )

                return {"choices": [choices["first_choice"], choices["second_choice"]]}

    def list_dashboard_recruitment_advisor_choice_students(
        self,
        *,
        choice_round: str,
        advisor_name: str | None = None,
        bucket: str | None = None,
    ) -> list[dict[str, Any]]:
        self.ensure_schema()
        normalized_choice_round = str(choice_round or "").strip()
        normalized_advisor_name = str(advisor_name or "").strip()
        normalized_bucket = str(bucket or "").strip().lower()
        if normalized_choice_round not in {"first_choice", "second_choice"}:
            return []

        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    WITH latest_application AS (
                        SELECT DISTINCT ON (ps.id)
                            ps.id AS portal_student_id,
                            ps.full_name AS student_name,
                            ps.phone_number,
                            ps.email,
                            ps.created_at AS registered_at,
                            ra.id AS recruitment_application_id,
                            ra.candidate_no,
                            NULLIF(BTRIM(ra.undergraduate_school), '') AS school_name,
                            NULLIF(BTRIM(ps.selected_advisor_name), '') AS selected_advisor_name,
                            NULLIF(BTRIM(ra.intended_advisor_name), '') AS intended_advisor_name,
                            NULLIF(BTRIM(pref1.advisor_name), '') AS first_choice_advisor_name,
                            NULLIF(BTRIM(pref2.advisor_name), '') AS second_choice_advisor_name
                        FROM dtlms_portal_students ps
                        JOIN dtlms_recruitment_applications ra ON ra.portal_student_id = ps.id AND ra.is_deleted = FALSE
                        LEFT JOIN LATERAL (
                            SELECT pref.advisor_name
                            FROM dtlms_portal_application_preferences pref
                            WHERE pref.application_id = ra.id
                              AND pref.preference_order = 1
                            ORDER BY pref.id ASC
                            LIMIT 1
                        ) pref1 ON TRUE
                        LEFT JOIN LATERAL (
                            SELECT pref.advisor_name
                            FROM dtlms_portal_application_preferences pref
                            WHERE pref.application_id = ra.id
                              AND pref.preference_order = 2
                            ORDER BY pref.id ASC
                            LIMIT 1
                        ) pref2 ON TRUE
                        ORDER BY ps.id, COALESCE(ra.applied_at, ra.created_at) DESC, ra.id DESC
                    ),
                    choice_rows AS (
                        SELECT
                            recruitment_application_id,
                            student_name,
                            phone_number,
                            email,
                            registered_at,
                            candidate_no,
                            school_name,
                            'first_choice' AS choice_round,
                            COALESCE(first_choice_advisor_name, selected_advisor_name, intended_advisor_name) AS advisor_name
                        FROM latest_application
                        UNION ALL
                        SELECT
                            recruitment_application_id,
                            student_name,
                            phone_number,
                            email,
                            registered_at,
                            candidate_no,
                            school_name,
                            'second_choice' AS choice_round,
                            second_choice_advisor_name AS advisor_name
                        FROM latest_application
                    ),
                    choice_counts AS (
                        SELECT choice_round, advisor_name, COUNT(*)::int AS student_count
                        FROM choice_rows
                        WHERE advisor_name IS NOT NULL AND BTRIM(advisor_name) <> ''
                        GROUP BY choice_round, advisor_name
                    ),
                    ranked_counts AS (
                        SELECT
                            choice_round,
                            advisor_name,
                            ROW_NUMBER() OVER (PARTITION BY choice_round ORDER BY student_count DESC, advisor_name ASC)::int AS advisor_rank
                        FROM choice_counts
                    ),
                    selected_advisors AS (
                        SELECT advisor_name
                        FROM ranked_counts
                        WHERE choice_round = %s
                          AND (
                              (%s = 'other' AND advisor_rank > 10)
                              OR (%s <> 'other' AND advisor_name = %s)
                          )
                    )
                    SELECT
                        cr.recruitment_application_id,
                        cr.student_name,
                        cr.choice_round,
                        cr.advisor_name,
                        cr.school_name,
                        cr.candidate_no,
                        cr.registered_at,
                        cr.phone_number,
                        cr.email
                    FROM choice_rows cr
                    JOIN selected_advisors sa ON sa.advisor_name = cr.advisor_name
                    WHERE cr.choice_round = %s
                    ORDER BY cr.registered_at DESC NULLS LAST, cr.recruitment_application_id DESC
                    """,
                    (
                        normalized_choice_round,
                        normalized_bucket,
                        normalized_bucket,
                        normalized_advisor_name,
                        normalized_choice_round,
                    ),
                )
                return [
                    {
                        "recruitment_application_id": int(row.get("recruitment_application_id") or 0),
                        "student_name": str(row.get("student_name") or ""),
                        "choice_round": str(row.get("choice_round") or ""),
                        "advisor_name": row.get("advisor_name"),
                        "school_name": row.get("school_name"),
                        "candidate_no": row.get("candidate_no"),
                        "registered_at": self._stringify_datetime(row.get("registered_at")),
                        "phone_number": row.get("phone_number"),
                        "email": row.get("email"),
                    }
                    for row in cur.fetchall()
                    if int(row.get("recruitment_application_id") or 0) > 0
                ]

    def list_theses_page(
        self,
        keyword: str | None = None,
        degree_status: str | None = None,
        advisor_name: str | None = None,
        thesis_status: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> tuple[list[dict[str, Any]], int]:
        self.ensure_schema()
        offset = max(page - 1, 0) * page_size
        where_clauses = ["t.is_deleted = FALSE"]
        params: list[Any] = []

        if degree_status:
            where_clauses.append(
                """
                CASE
                    WHEN t.degree_granted = 'reviewing' THEN '授位审批中'
                    WHEN t.degree_granted = 'granted' THEN '已授位'
                    WHEN t.defense_date IS NOT NULL THEN '待正式答辩'
                    ELSE '待申请'
                END = %s
                """
            )
            params.append(degree_status)
        if advisor_name:
            where_clauses.append("COALESCE(a.full_name, '') = %s")
            params.append(advisor_name)
        if thesis_status:
            where_clauses.append(
                """
                CASE
                    WHEN t.thesis_status = 'plagiarism_passed' THEN '查重通过'
                    WHEN t.thesis_status = 'review_passed' THEN '盲审通过'
                    WHEN t.thesis_status = 'rework' THEN '退回修改'
                    ELSE '待查重'
                END = %s
                """
            )
            params.append(thesis_status)
        if keyword and str(keyword).strip():
            keyword_like = f"%{str(keyword).strip()}%"
            where_clauses.append(
                """
                (
                    t.business_key ILIKE %s
                    OR s.student_no ILIKE %s
                    OR s.full_name ILIKE %s
                    OR t.title ILIKE %s
                )
                """
            )
            params.extend([keyword_like, keyword_like, keyword_like, keyword_like])

        where_sql = " AND ".join(where_clauses)
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                self._execute_dynamic(
                    cur,
                    f"""
                    SELECT COUNT(*) AS total
                    FROM dtlms_theses t
                    JOIN dtlms_students s ON s.id = t.student_id AND s.is_deleted = FALSE
                    JOIN dtlms_advisors a ON a.id = t.advisor_id AND a.is_deleted = FALSE
                    WHERE {where_sql}
                    """,
                    params,
                )
                total_row = cur.fetchone()
                total = int(total_row["total"] if total_row else 0)
                self._execute_dynamic(
                    cur,
                    f"""
                    SELECT
                        t.id,
                        t.business_key,
                        s.student_no,
                        s.full_name AS student_name,
                        a.full_name AS advisor_name,
                        t.title,
                        t.plagiarism_rate,
                        t.thesis_status,
                        t.blind_review_status,
                        t.defense_date,
                        t.degree_granted
                    FROM dtlms_theses t
                    JOIN dtlms_students s ON s.id = t.student_id AND s.is_deleted = FALSE
                    JOIN dtlms_advisors a ON a.id = t.advisor_id AND a.is_deleted = FALSE
                    WHERE {where_sql}
                    ORDER BY t.id DESC
                    LIMIT %s OFFSET %s
                    """,
                    [*params, page_size, offset],
                )
                return [self._normalize_thesis_row(dict(row)) for row in cur.fetchall()], total

    def list_thesis_reviews_page(
        self,
        thesis_id: int | None = None,
        keyword: str | None = None,
        expert_name: str | None = None,
        review_status: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> tuple[list[dict[str, Any]], int]:
        self.ensure_schema()
        offset = max(page - 1, 0) * page_size
        where_clauses = ["1 = 1"]
        params: list[Any] = []
        if thesis_id is not None:
            where_clauses.append("tr.thesis_id = %s")
            params.append(int(thesis_id))
        if expert_name:
            where_clauses.append("tr.expert_name = %s")
            params.append(expert_name)
        if review_status:
            where_clauses.append(
                """
                CASE
                    WHEN tr.review_status = 'approved' THEN '通过'
                    WHEN tr.review_status = 'rejected' THEN '不通过'
                    ELSE '待审阅'
                END = %s
                """
            )
            params.append(review_status)
        if keyword and str(keyword).strip():
            keyword_like = f"%{str(keyword).strip()}%"
            where_clauses.append(
                """
                (
                    t.title ILIKE %s
                    OR tr.expert_name ILIKE %s
                    OR COALESCE(tr.review_comment, '') ILIKE %s
                )
                """
            )
            params.extend([keyword_like, keyword_like, keyword_like])

        where_sql = " AND ".join(where_clauses)
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                self._execute_dynamic(
                    cur,
                    f"""
                    SELECT COUNT(*) AS total
                    FROM dtlms_thesis_reviews tr
                    JOIN dtlms_theses t ON t.id = tr.thesis_id AND t.is_deleted = FALSE
                    WHERE {where_sql}
                    """,
                    params,
                )
                total_row = cur.fetchone()
                total = int(total_row["total"] if total_row else 0)
                self._execute_dynamic(
                    cur,
                    f"""
                    SELECT
                        tr.id,
                        tr.thesis_id,
                        t.title AS thesis_title,
                        tr.expert_name,
                        tr.review_score,
                        tr.review_status,
                        tr.review_comment
                    FROM dtlms_thesis_reviews tr
                    JOIN dtlms_theses t ON t.id = tr.thesis_id AND t.is_deleted = FALSE
                    WHERE {where_sql}
                    ORDER BY tr.id DESC
                    LIMIT %s OFFSET %s
                    """,
                    [*params, page_size, offset],
                )
                return [self._normalize_thesis_review_row(dict(row)) for row in cur.fetchall()], total

    def list_operation_logs_page(
        self,
        keyword: str | None = None,
        module_name: str | None = None,
        result: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> tuple[list[dict[str, Any]], int]:
        self.ensure_schema()
        offset = max(page - 1, 0) * page_size
        where_clauses = ["1 = 1"]
        params: list[Any] = []

        if keyword and str(keyword).strip():
            where_clauses.append(
                """
                (
                    operator_username ILIKE %s
                    OR entity_name ILIKE %s
                    OR COALESCE(new_value->>'summary', '') ILIKE %s
                )
                """
            )
            keyword_like = f"%{str(keyword).strip()}%"
            params.extend([keyword_like, keyword_like, keyword_like])
        if module_name:
            where_clauses.append("module_name = %s")
            params.append(module_name)
        if result:
            where_clauses.append("result = %s")
            params.append(result)

        where_sql = " AND ".join(where_clauses)

        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                self._execute_dynamic(
                    cur,
                    f"SELECT COUNT(*) AS total FROM dtlms_operation_logs WHERE {where_sql}",
                    params,
                )
                total_row = cur.fetchone()
                total = int(total_row["total"] if total_row else 0)

                self._execute_dynamic(
                    cur,
                    f"""
                    SELECT id, created_at, operator_username, module_name, entity_name, entity_id, action, result, new_value
                    FROM dtlms_operation_logs
                    WHERE {where_sql}
                    ORDER BY created_at DESC, id DESC
                    LIMIT %s OFFSET %s
                    """,
                    [*params, page_size, offset],
                )
                return [self._normalize_operation_log_row(dict(row)) for row in cur.fetchall()], total

    def list_recruitment_applications_page(
        self,
        keyword: str | None = None,
        plan_id: int | None = None,
        status: str | None = None,
        portal_student_only: bool = False,
        advisor_name: str | None = None,
        advisor_names: list[str] | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> tuple[list[dict[str, Any]], int]:
        self.ensure_schema()
        offset = max(page - 1, 0) * page_size
        where_clauses = ["ra.is_deleted = FALSE"]
        params: list[Any] = []

        if plan_id is not None:
            where_clauses.append("ra.plan_id = %s")
            params.append(int(plan_id))
        if portal_student_only:
            where_clauses.append("ra.portal_student_id IS NOT NULL")
        if status:
            status_filters = [
                self._map_application_status(item)
                for item in (segment.strip() for segment in str(status).split(","))
                if item
            ]
            if len(status_filters) == 1:
                where_clauses.append("ra.application_status = %s")
                params.append(status_filters[0])
            elif status_filters:
                where_clauses.append("ra.application_status = ANY(%s)")
                params.append(status_filters)
        if advisor_name and str(advisor_name).strip():
            normalized_advisor_name = str(advisor_name).strip()
            where_clauses.append(
                """
                (
                    (
                        COALESCE(ra.advisor_screening_round, '') = 'second_choice'
                        AND COALESCE(ra.second_choice, '') = %s
                    )
                    OR
                    (
                        COALESCE(ra.advisor_screening_round, '') <> 'second_choice'
                        AND COALESCE(NULLIF(ra.first_choice, ''), ra.intended_advisor_name, '') = %s
                    )
                )
                """
            )
            params.extend([normalized_advisor_name, normalized_advisor_name])
        normalized_advisor_names = [str(item).strip() for item in (advisor_names or []) if str(item).strip()]
        if normalized_advisor_names:
            where_clauses.append(
                """
                (
                    (
                        COALESCE(ra.advisor_screening_round, '') = 'second_choice'
                        AND COALESCE(ra.second_choice, '') = ANY(%s)
                    )
                    OR
                    (
                        COALESCE(ra.advisor_screening_round, '') <> 'second_choice'
                        AND COALESCE(NULLIF(ra.first_choice, ''), ra.intended_advisor_name, '') = ANY(%s)
                    )
                )
                """
            )
            params.extend([normalized_advisor_names, normalized_advisor_names])
        if keyword and str(keyword).strip():
            keyword_like = f"%{str(keyword).strip()}%"
            where_clauses.append(
                """
                (
                    COALESCE(ra.business_key, '') ILIKE %s
                    OR COALESCE(ra.candidate_no, '') ILIKE %s
                    OR COALESCE(ra.student_name, '') ILIKE %s
                    OR COALESCE(ra.graduation_school, '') ILIKE %s
                    OR COALESCE(ra.graduate_school, '') ILIKE %s
                    OR COALESCE(rf.field_name, '') ILIKE %s
                    OR COALESCE(ra.first_choice, '') ILIKE %s
                    OR COALESCE(ra.second_choice, '') ILIKE %s
                    OR COALESCE(ra.intended_advisor_name, '') ILIKE %s
                    OR COALESCE(ra.phone_number, '') ILIKE %s
                    OR COALESCE(ra.email, '') ILIKE %s
                )
                """
            )
            params.extend([keyword_like] * 11)

        where_sql = " AND ".join(where_clauses)

        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                count_sql = f"""
                    SELECT COUNT(*) AS total
                    FROM dtlms_recruitment_applications ra
                    LEFT JOIN dtlms_research_fields rf ON rf.id = ra.intended_field_id AND rf.is_deleted = FALSE
                    WHERE {where_sql}
                """
                self._execute_dynamic(cur, count_sql, params)
                total_row = cur.fetchone()
                total = int(total_row["total"] if total_row else 0)

                page_sql = f"""
                    SELECT
                        ra.*,
                        CASE WHEN COALESCE(ps.account_status, 'active') = 'inactive' THEN '停用' ELSE '启用' END AS account_status,
                        rp.plan_name AS selected_plan_name,
                        ps.created_at AS registered_at,
                        rf.field_name AS intended_field,
                        am.material_status,
                        qr.reviewer_username AS reviewer_name,
                        ad.final_score
                    FROM dtlms_recruitment_applications ra
                    LEFT JOIN dtlms_portal_students ps ON ps.id = ra.portal_student_id
                    LEFT JOIN dtlms_recruitment_plans rp ON rp.id = ra.plan_id
                    LEFT JOIN dtlms_research_fields rf ON rf.id = ra.intended_field_id AND rf.is_deleted = FALSE
                    LEFT JOIN LATERAL (
                        SELECT material_status
                        FROM dtlms_application_materials
                        WHERE application_id = ra.id AND is_deleted = FALSE
                        ORDER BY updated_at DESC, id DESC
                        LIMIT 1
                    ) am ON TRUE
                    LEFT JOIN LATERAL (
                        SELECT reviewer_username
                        FROM dtlms_qualification_reviews
                        WHERE application_id = ra.id
                        ORDER BY updated_at DESC, id DESC
                        LIMIT 1
                    ) qr ON TRUE
                    LEFT JOIN LATERAL (
                        SELECT final_score
                        FROM dtlms_admission_decisions
                        WHERE application_id = ra.id
                        ORDER BY updated_at DESC, id DESC
                        LIMIT 1
                    ) ad ON TRUE
                    WHERE {where_sql}
                    ORDER BY COALESCE(ra.applied_at, ra.created_at) DESC, ra.id DESC
                    LIMIT %s OFFSET %s
                """
                self._execute_dynamic(cur, page_sql, [*params, page_size, offset])
                return [self._normalize_recruitment_application_row(dict(row)) for row in cur.fetchall()], total

    def list_centers_page(
        self,
        keyword: str | None = None,
        is_enabled: bool | None = None,
        director_id: int | None = None,
        principal: Any | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> tuple[list[dict[str, Any]], int]:
        self.ensure_schema()
        offset = max(page - 1, 0) * page_size
        where_clauses = ["t.is_deleted = FALSE"]
        params: list[Any] = []

        if keyword and str(keyword).strip():
            keyword_like = f"%{str(keyword).strip()}%"
            where_clauses.append(
                """
                (
                    t.team_name ILIKE %s
                    OR COALESCE(lead.full_name, '') ILIKE %s
                    OR EXISTS (
                        SELECT 1
                        FROM dtlms_team_advisors ta_keyword
                        JOIN dtlms_advisors advisor_keyword ON advisor_keyword.id = ta_keyword.advisor_id AND advisor_keyword.is_deleted = FALSE
                        WHERE ta_keyword.team_id = t.id
                          AND ta_keyword.is_deleted = FALSE
                          AND advisor_keyword.full_name ILIKE %s
                    )
                )
                """
            )
            params.extend([keyword_like] * 3)
        if is_enabled is not None:
            where_clauses.append("t.team_status = %s" if is_enabled else "t.team_status <> %s")
            params.append("active")
        if director_id:
            where_clauses.append("COALESCE(t.lead_user_id, lead.user_id, 0) = %s")
            params.append(int(director_id))
        if self._needs_center_scope_filter(principal):
            username = str(self._principal_field_value(principal, "username") or "").strip()
            if not username:
                return [], 0
            where_clauses.append(
                """
                (
                    COALESCE(t.lead_user_id, lead.user_id, 0) = (
                        SELECT u.id
                        FROM dtlms_users u
                        WHERE u.username = %s
                          AND u.is_deleted = FALSE
                        LIMIT 1
                    )
                    OR EXISTS (
                        SELECT 1
                        FROM dtlms_team_advisors ta_scope
                        LEFT JOIN dtlms_advisors advisor_scope ON advisor_scope.id = ta_scope.advisor_id AND advisor_scope.is_deleted = FALSE
                        WHERE ta_scope.team_id = t.id
                          AND ta_scope.is_deleted = FALSE
                          AND COALESCE(ta_scope.advisor_user_id, advisor_scope.user_id, 0) = (
                              SELECT u.id
                              FROM dtlms_users u
                              WHERE u.username = %s
                                AND u.is_deleted = FALSE
                              LIMIT 1
                          )
                    )
                )
                """
            )
            params.extend([username, username])

        where_sql = " AND ".join(where_clauses)

        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                count_sql = f"""
                    SELECT COUNT(*) AS total
                    FROM dtlms_teams t
                    LEFT JOIN dtlms_advisors lead ON lead.id = t.lead_advisor_id AND lead.is_deleted = FALSE
                    WHERE {where_sql}
                """
                self._execute_dynamic(cur, count_sql, params)
                total_row = cur.fetchone()
                total = int(total_row["total"] if total_row else 0)

                page_sql = f"""
                    SELECT
                        t.id,
                        t.team_name,
                        COALESCE(t.lead_user_id, lead.user_id) AS director_id,
                        lead.full_name AS director_name,
                        COALESCE(advisor_names.advisor_names, '') AS advisor_names,
                        COALESCE(advisor_names.advisor_ids, ARRAY[]::bigint[]) AS advisor_ids,
                        COALESCE(advisor_names.advisor_relation_ids, ARRAY[]::bigint[]) AS advisor_relation_ids,
                        t.team_status,
                        COALESCE(TO_CHAR(t.established_on, 'YYYY-MM-DD'), TO_CHAR(t.created_at::date, 'YYYY-MM-DD')) AS created_date,
                        COALESCE(student_stats.member_student_count, 0) AS member_student_count,
                        COALESCE(student_stats.active_student_count, 0) AS active_student_count
                    FROM dtlms_teams t
                    LEFT JOIN dtlms_advisors lead ON lead.id = t.lead_advisor_id AND lead.is_deleted = FALSE
                    LEFT JOIN LATERAL (
                        SELECT
                            string_agg(advisor_rows.advisor_name, '、' ORDER BY advisor_rows.sort_role, advisor_rows.advisor_name, advisor_rows.relation_id) AS advisor_names,
                            array_agg(advisor_rows.advisor_user_id ORDER BY advisor_rows.sort_role, advisor_rows.advisor_name, advisor_rows.relation_id) AS advisor_ids,
                            array_agg(advisor_rows.relation_id ORDER BY advisor_rows.sort_role, advisor_rows.advisor_name, advisor_rows.relation_id) AS advisor_relation_ids
                        FROM (
                            SELECT DISTINCT
                                ta.id AS relation_id,
                                COALESCE(ta.advisor_user_id, advisor.user_id) AS advisor_user_id,
                                advisor.full_name AS advisor_name,
                                CASE WHEN ta.advisor_role = 'lead' THEN 0 ELSE 1 END AS sort_role
                            FROM dtlms_team_advisors ta
                            JOIN dtlms_advisors advisor ON advisor.id = ta.advisor_id AND advisor.is_deleted = FALSE
                            WHERE ta.team_id = t.id AND ta.is_deleted = FALSE
                        ) advisor_rows
                    ) advisor_names ON TRUE
                    LEFT JOIN LATERAL (
                        SELECT
                            COUNT(*) AS member_student_count,
                            COUNT(*) FILTER (WHERE s.current_status IN ('enrolled', 'internship', 'outbound', 'thesis')) AS active_student_count
                        FROM dtlms_students s
                        WHERE s.team_id = t.id AND s.is_deleted = FALSE
                    ) student_stats ON TRUE
                    WHERE {where_sql}
                    ORDER BY t.id DESC
                    LIMIT %s OFFSET %s
                """
                self._execute_dynamic(cur, page_sql, [*params, page_size, offset])
                return [self._normalize_center_row(dict(row)) for row in cur.fetchall()], total

    def list_active_advisors(self) -> list[dict[str, Any]]:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                                        SELECT
                                                u.id,
                                                u.full_name,
                                                advisor_match.advisor_no,
                                                COALESCE(advisor_match.organization_name, NULLIF(u.department_name, ''), '未分配单位') AS organization_name,
                                                NULLIF(up.introduction, '') AS introduction
                                        FROM dtlms_users u
                                        JOIN dtlms_user_roles ur ON ur.user_id = u.id
                                        JOIN dtlms_roles r ON r.id = ur.role_id AND r.is_deleted = FALSE
                                        LEFT JOIN dtlms_user_profiles up ON up.username = u.username
                                        LEFT JOIN LATERAL (
                                                SELECT a.advisor_no, a.organization_name
                                                FROM dtlms_advisors a
                                                WHERE a.is_deleted = FALSE
                                                    AND a.user_id = u.id
                                                ORDER BY a.id
                                                LIMIT 1
                                        ) advisor_match ON TRUE
                                        WHERE u.is_deleted = FALSE
                                            AND u.is_active = TRUE
                                            AND r.role_code = 'advisor'
                                        ORDER BY u.full_name ASC, u.id ASC
                    """
                )
                rows = [dict(row) for row in cur.fetchall()]
                if not rows:
                    cur.execute(
                        """
                                                SELECT id, full_name, NULL::varchar AS advisor_no, department_name AS organization_name, NULL::text AS introduction
                                                FROM dtlms_users
                                                WHERE is_deleted = FALSE
                                                    AND is_active = TRUE
                                                ORDER BY full_name ASC, id ASC
                        """
                    )
                    rows = [dict(row) for row in cur.fetchall()]
                return rows

    def list_sync_logs_page(
        self,
        keyword: str | None = None,
        sync_status: str | None = None,
        source_system: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> tuple[list[dict[str, Any]], int]:
        self.ensure_schema()
        offset = max(page - 1, 0) * page_size
        where_clauses = ["1 = 1"]
        params: list[Any] = []

        if keyword and str(keyword).strip():
            keyword_like = f"%{str(keyword).strip()}%"
            where_clauses.append(
                """
                (
                    source_system ILIKE %s
                    OR target_system ILIKE %s
                    OR COALESCE(failure_reason, '') ILIKE %s
                )
                """
            )
            params.extend([keyword_like, keyword_like, keyword_like])
        if sync_status:
            where_clauses.append("sync_status = %s")
            params.append(sync_status)
        if source_system:
            where_clauses.append("source_system = %s")
            params.append(source_system)

        where_sql = " AND ".join(where_clauses)

        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                self._execute_dynamic(
                    cur,
                    f"SELECT COUNT(*) AS total FROM dtlms_data_sync_logs WHERE {where_sql}",
                    params,
                )
                total_row = cur.fetchone()
                total = int(total_row["total"] if total_row else 0)

                self._execute_dynamic(
                    cur,
                    f"""
                    SELECT id, source_system, target_system, sync_status, record_count, created_at, failure_reason
                    FROM dtlms_data_sync_logs
                    WHERE {where_sql}
                    ORDER BY created_at DESC, id DESC
                    LIMIT %s OFFSET %s
                    """,
                    [*params, page_size, offset],
                )
                return [self._normalize_sync_log_row(dict(row)) for row in cur.fetchall()], total

    def list_notification_delivery_logs_page(
        self,
        keyword: str | None = None,
        channel: str | None = None,
        send_status: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> tuple[list[dict[str, Any]], int]:
        self.ensure_schema()
        offset = max(page - 1, 0) * page_size
        where_clauses = ["1 = 1"]
        params: list[Any] = []

        if keyword and str(keyword).strip():
            keyword_like = f"%{str(keyword).strip()}%"
            where_clauses.append(
                """
                (
                    recipient ILIKE %s
                    OR subject ILIKE %s
                    OR COALESCE(template_code, '') ILIKE %s
                    OR COALESCE(failure_reason, '') ILIKE %s
                    OR COALESCE(business_key, '') ILIKE %s
                )
                """
            )
            params.extend([keyword_like] * 5)
        if channel:
            where_clauses.append("channel = %s")
            params.append(channel)
        if send_status:
            where_clauses.append("send_status = %s")
            params.append(send_status)

        where_sql = " AND ".join(where_clauses)

        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                self._execute_dynamic(
                    cur,
                    f"SELECT COUNT(*) AS total FROM dtlms_notification_delivery_logs WHERE {where_sql}",
                    params,
                )
                total_row = cur.fetchone()
                total = int(total_row["total"] if total_row else 0)

                self._execute_dynamic(
                    cur,
                    f"""
                    SELECT id, channel, template_code, recipient, subject, send_status, failure_reason, business_key, triggered_by, created_at
                    FROM dtlms_notification_delivery_logs
                    WHERE {where_sql}
                    ORDER BY created_at DESC, id DESC
                    LIMIT %s OFFSET %s
                    """,
                    [*params, page_size, offset],
                )
                return [self._normalize_notification_delivery_log_row(dict(row)) for row in cur.fetchall()], total

    def list_roles_page(
        self,
        keyword: str | None = None,
        scope_name: str | None = None,
        permission: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> tuple[list[dict[str, Any]], int]:
        self.ensure_schema()
        offset = max(page - 1, 0) * page_size
        where_clauses = ["r.is_deleted = FALSE"]
        params: list[Any] = []
        if keyword and str(keyword).strip():
            keyword_like = f"%{str(keyword).strip()}%"
            where_clauses.append("(r.role_code ILIKE %s OR r.role_name ILIKE %s OR COALESCE(r.scope_name, '') ILIKE %s)")
            params.extend([keyword_like, keyword_like, keyword_like])
        if scope_name:
            where_clauses.append("COALESCE(r.scope_name, '') = %s")
            params.append(scope_name)
        if permission:
            where_clauses.append(
                "EXISTS (SELECT 1 FROM dtlms_role_permissions rp2 JOIN dtlms_permissions p2 ON p2.id = rp2.permission_id AND p2.is_deleted = FALSE WHERE rp2.role_id = r.id AND p2.permission_code = %s)"
            )
            params.append(permission)
        where_sql = " AND ".join(where_clauses)
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                self._execute_dynamic(cur, f"SELECT COUNT(*) AS total FROM dtlms_roles r WHERE {where_sql}", params)
                total_row = cur.fetchone()
                total = int(total_row["total"] if total_row else 0)
                self._execute_dynamic(
                    cur,
                    f"""
                    SELECT
                        r.id,
                        r.role_code,
                        r.role_name,
                        COALESCE(r.scope_name, '系统管理') AS scope_name,
                        COALESCE(array_agg(DISTINCT p.permission_code) FILTER (WHERE p.permission_code IS NOT NULL), ARRAY[]::varchar[]) AS permissions,
                        COUNT(DISTINCT ur.user_id) FILTER (WHERE u.is_deleted = FALSE) AS user_count
                    FROM dtlms_roles r
                    LEFT JOIN dtlms_role_permissions rp ON rp.role_id = r.id
                    LEFT JOIN dtlms_permissions p ON p.id = rp.permission_id AND p.is_deleted = FALSE
                    LEFT JOIN dtlms_user_roles ur ON ur.role_id = r.id
                    LEFT JOIN dtlms_users u ON u.id = ur.user_id
                    WHERE {where_sql}
                    GROUP BY r.id
                    ORDER BY r.id DESC
                    LIMIT %s OFFSET %s
                    """,
                    [*params, page_size, offset],
                )
                return [self._normalize_role_row(dict(row)) for row in cur.fetchall()], total

    def list_audit_policies_page(
        self,
        keyword: str | None = None,
        status: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> tuple[list[dict[str, Any]], int]:
        self.ensure_schema()
        offset = max(page - 1, 0) * page_size
        where_clauses = ["is_deleted = FALSE"]
        params: list[Any] = []
        if keyword and str(keyword).strip():
            keyword_like = f"%{str(keyword).strip()}%"
            where_clauses.append("(item ILIKE %s OR policy ILIKE %s)")
            params.extend([keyword_like, keyword_like])
        if status:
            where_clauses.append("status = %s")
            params.append(status)
        where_sql = " AND ".join(where_clauses)
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                self._execute_dynamic(cur, f"SELECT COUNT(*) AS total FROM dtlms_audit_policies WHERE {where_sql}", params)
                total_row = cur.fetchone()
                total = int(total_row["total"] if total_row else 0)
                self._execute_dynamic(
                    cur,
                    f"SELECT id, item, policy, status FROM dtlms_audit_policies WHERE {where_sql} ORDER BY id DESC LIMIT %s OFFSET %s",
                    [*params, page_size, offset],
                )
                return [self._normalize_audit_policy_row(dict(row)) for row in cur.fetchall()], total

    def list_integrations_page(
        self,
        keyword: str | None = None,
        status: str | None = None,
        direction: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> tuple[list[dict[str, Any]], int]:
        self.ensure_schema()
        offset = max(page - 1, 0) * page_size
        where_clauses = ["is_deleted = FALSE"]
        params: list[Any] = []
        if keyword and str(keyword).strip():
            keyword_like = f"%{str(keyword).strip()}%"
            where_clauses.append("(name ILIKE %s OR owner ILIKE %s OR direction ILIKE %s)")
            params.extend([keyword_like, keyword_like, keyword_like])
        if status:
            where_clauses.append("status = %s")
            params.append(status)
        if direction:
            where_clauses.append("direction = %s")
            params.append(direction)
        where_sql = " AND ".join(where_clauses)
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                self._execute_dynamic(cur, f"SELECT COUNT(*) AS total FROM dtlms_integrations WHERE {where_sql}", params)
                total_row = cur.fetchone()
                total = int(total_row["total"] if total_row else 0)
                self._execute_dynamic(
                    cur,
                    f"SELECT id, name, direction, cadence, status, owner FROM dtlms_integrations WHERE {where_sql} ORDER BY id DESC LIMIT %s OFFSET %s",
                    [*params, page_size, offset],
                )
                return [self._normalize_integration_row(dict(row)) for row in cur.fetchall()], total

    def list_system_users_page(
        self,
        keyword: str | None = None,
        role_code: str | None = None,
        account_status: str | None = None,
        department_name: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> tuple[list[dict[str, Any]], int]:
        self.ensure_schema()
        offset = max(page - 1, 0) * page_size
        where_clauses = ["u.is_deleted = FALSE"]
        params: list[Any] = []

        if keyword and str(keyword).strip():
            keyword_like = f"%{str(keyword).strip()}%"
            where_clauses.append(
                """
                (
                    COALESCE(u.username, '') ILIKE %s
                    OR COALESCE(u.full_name, '') ILIKE %s
                    OR COALESCE(up.department_name, u.department_name, '') ILIKE %s
                )
                """
            )
            params.extend([keyword_like, keyword_like, keyword_like])
        if role_code:
            where_clauses.append("COALESCE(r.role_code, '') = %s")
            params.append(role_code)
        if account_status:
            where_clauses.append("CASE WHEN u.is_active THEN '启用' ELSE '停用' END = %s")
            params.append(account_status)
        if department_name:
            where_clauses.append("COALESCE(up.department_name, u.department_name, '') ILIKE %s")
            params.append(f"%{department_name}%")

        where_sql = " AND ".join(where_clauses)

        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                self._execute_dynamic(
                    cur,
                    f"""
                    SELECT COUNT(*) AS total
                    FROM dtlms_users u
                    LEFT JOIN dtlms_user_roles ur ON ur.user_id = u.id
                    LEFT JOIN dtlms_roles r ON r.id = ur.role_id AND r.is_deleted = FALSE
                    LEFT JOIN dtlms_user_profiles up ON up.username = u.username
                    WHERE {where_sql}
                    """,
                    params,
                )
                total_row = cur.fetchone()
                total = int(total_row["total"] if total_row else 0)

                self._execute_dynamic(
                    cur,
                    f"""
                    SELECT
                        u.id,
                        u.username,
                        u.full_name,
                        COALESCE(r.role_code, '') AS role_code,
                        COALESCE(r.role_name, '') AS role_name,
                        COALESCE(up.department_name, u.department_name, '') AS department_name,
                        up.introduction AS introduction,
                        up.email AS email,
                        COALESCE(up.phone_number, u.phone_number) AS phone_number,
                        CASE WHEN u.is_active THEN '启用' ELSE '停用' END AS account_status,
                        u.last_login_at
                    FROM dtlms_users u
                    LEFT JOIN dtlms_user_roles ur ON ur.user_id = u.id
                    LEFT JOIN dtlms_roles r ON r.id = ur.role_id AND r.is_deleted = FALSE
                    LEFT JOIN dtlms_user_profiles up ON up.username = u.username
                    WHERE {where_sql}
                    ORDER BY u.id DESC
                    LIMIT %s OFFSET %s
                    """,
                    [*params, page_size, offset],
                )
                return [self._normalize_system_user_row(dict(row)) for row in cur.fetchall()], total

    def list_dict_types(self, keyword: str | None = None, status: str | None = None) -> list[dict[str, Any]]:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                where_clauses = ["t.is_deleted = FALSE"]
                params: list[Any] = []
                if status:
                    where_clauses.append("t.status = %s")
                    params.append(status)
                if keyword:
                    where_clauses.append("(t.dict_name ILIKE %s OR t.dict_type ILIKE %s)")
                    params.extend([f"%{keyword}%", f"%{keyword}%"])
                sql_text = f"""
                    SELECT t.id, t.dict_name, t.dict_type, t.status, t.remark, COUNT(d.id) AS data_count
                    FROM dtlms_dict_types t
                    LEFT JOIN dtlms_dict_data d ON d.dict_type_id = t.id AND d.is_deleted = FALSE
                    WHERE {' AND '.join(where_clauses)}
                    GROUP BY t.id
                    ORDER BY t.id DESC
                """
                self._execute_dynamic(cur, sql_text, params)
                return [self._normalize_dict_row(dict(row) | {"data_count": int(row["data_count"])} ) for row in cur.fetchall()]

    def list_dict_data(self, keyword: str | None = None, dict_type: str | None = None, status: str | None = None) -> list[dict[str, Any]]:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                where_clauses = ["d.is_deleted = FALSE", "t.is_deleted = FALSE"]
                params: list[Any] = []
                if dict_type:
                    where_clauses.append("d.dict_type = %s")
                    params.append(dict_type)
                if status:
                    where_clauses.append("d.status = %s")
                    params.append(status)
                if keyword:
                    where_clauses.append("(d.label ILIKE %s OR d.value ILIKE %s OR d.dict_type ILIKE %s)")
                    params.extend([f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"])
                sql_text = f"""
                    SELECT d.id, d.dict_type, t.dict_name, d.label, d.value, d.sort_order, d.status, d.color_type, d.css_class, d.remark
                    FROM dtlms_dict_data d
                    JOIN dtlms_dict_types t ON t.id = d.dict_type_id
                    WHERE {' AND '.join(where_clauses)}
                    ORDER BY d.dict_type ASC, d.sort_order ASC, d.id ASC
                """
                self._execute_dynamic(cur, sql_text, params)
                return [self._normalize_dict_row(dict(row)) for row in cur.fetchall()]

    def list_news_articles(self, keyword: str | None = None, news_type: str | None = None, status: str | None = None) -> list[dict[str, Any]]:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                where_clauses = ["is_deleted = FALSE"]
                params: list[Any] = []
                if news_type:
                    where_clauses.append("news_type = %s")
                    params.append(news_type)
                if status:
                    where_clauses.append("status = %s")
                    params.append(status)
                if keyword:
                    where_clauses.append("(news_title ILIKE %s OR news_content ILIKE %s OR news_code ILIKE %s OR publisher_name ILIKE %s OR reviewer_name ILIKE %s)")
                    params.extend([f"%{keyword}%"] * 5)
                sql_text = f"""
                    SELECT
                        id,
                        news_code,
                        news_title,
                        news_content,
                        news_type,
                        publisher_user_id,
                        publisher_username,
                        publisher_name,
                        reviewer_user_id,
                        reviewer_username,
                        reviewer_name,
                        published_at,
                        status,
                        is_pinned,
                        display_order,
                        created_at,
                        updated_at
                    FROM dtlms_news_articles
                    WHERE {' AND '.join(where_clauses)}
                    ORDER BY is_pinned DESC, published_at DESC NULLS LAST, display_order DESC, id DESC
                """
                self._execute_dynamic(cur, sql_text, params)
                return [self._normalize_news_row(dict(row)) for row in cur.fetchall()]

    def get_news_article_by_id(self, news_article_id: int) -> dict[str, Any] | None:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        id,
                        news_code,
                        news_title,
                        news_content,
                        news_type,
                        publisher_user_id,
                        publisher_username,
                        publisher_name,
                        reviewer_user_id,
                        reviewer_username,
                        reviewer_name,
                        published_at,
                        status,
                        is_pinned,
                        display_order,
                        created_at,
                        updated_at
                    FROM dtlms_news_articles
                    WHERE id = %s AND is_deleted = FALSE
                    LIMIT 1
                    """,
                    (int(news_article_id),),
                )
                row = cur.fetchone()
                return self._normalize_news_row(dict(row)) if row is not None else None

    def create_news_article(self, payload: dict[str, Any]) -> dict[str, Any]:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO dtlms_news_articles (
                        news_code,
                        news_title,
                        news_content,
                        news_type,
                        publisher_user_id,
                        publisher_username,
                        publisher_name,
                        reviewer_user_id,
                        reviewer_username,
                        reviewer_name,
                        published_at,
                        status,
                        is_pinned,
                        display_order
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING
                        id,
                        news_code,
                        news_title,
                        news_content,
                        news_type,
                        publisher_user_id,
                        publisher_username,
                        publisher_name,
                        reviewer_user_id,
                        reviewer_username,
                        reviewer_name,
                        published_at,
                        status,
                        is_pinned,
                        display_order,
                        created_at,
                        updated_at
                    """,
                    (
                        payload["news_code"],
                        payload["news_title"],
                        payload["news_content"],
                        payload["news_type"],
                        payload.get("publisher_user_id"),
                        payload.get("publisher_username"),
                        payload.get("publisher_name"),
                        payload.get("reviewer_user_id"),
                        payload.get("reviewer_username"),
                        payload.get("reviewer_name"),
                        payload.get("published_at"),
                        payload.get("status", "草稿"),
                        bool(payload.get("is_pinned", False)),
                        int(payload.get("display_order", 0)),
                    ),
                )
                record = self._normalize_news_row(self._require_row(cur.fetchone(), "create_news_article"))
            conn.commit()
        return record

    def update_news_article(self, news_article_id: int, payload: dict[str, Any]) -> dict[str, Any]:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM dtlms_news_articles WHERE id = %s AND is_deleted = FALSE", (int(news_article_id),))
                if not cur.fetchone():
                    raise KeyError(news_article_id)
                cur.execute(
                    """
                    UPDATE dtlms_news_articles
                    SET news_title = %s,
                        news_content = %s,
                        news_type = %s,
                        published_at = %s,
                        status = %s,
                        is_pinned = %s,
                        display_order = %s,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                    RETURNING
                        id,
                        news_code,
                        news_title,
                        news_content,
                        news_type,
                        publisher_user_id,
                        publisher_username,
                        publisher_name,
                        reviewer_user_id,
                        reviewer_username,
                        reviewer_name,
                        published_at,
                        status,
                        is_pinned,
                        display_order,
                        created_at,
                        updated_at
                    """,
                    (
                        payload["news_title"],
                        payload["news_content"],
                        payload["news_type"],
                        payload.get("published_at"),
                        payload.get("status", "草稿"),
                        bool(payload.get("is_pinned", False)),
                        int(payload.get("display_order", 0)),
                        int(news_article_id),
                    ),
                )
                record = self._normalize_news_row(self._require_row(cur.fetchone(), "update_news_article"))
            conn.commit()
        return record

    def delete_news_article(self, news_article_id: int) -> None:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM dtlms_news_articles WHERE id = %s AND is_deleted = FALSE", (int(news_article_id),))
                if not cur.fetchone():
                    raise KeyError(news_article_id)
                cur.execute(
                    "UPDATE dtlms_news_articles SET is_deleted = TRUE, updated_at = CURRENT_TIMESTAMP WHERE id = %s",
                    (int(news_article_id),),
                )
            conn.commit()

    def publish_news_article(
        self,
        news_article_id: int,
        *,
        publisher_username: str | None = None,
        publisher_name: str | None = None,
    ) -> dict[str, Any]:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE dtlms_news_articles
                    SET status = '已发布',
                        published_at = COALESCE(published_at, CURRENT_TIMESTAMP),
                        publisher_username = COALESCE(%s, publisher_username),
                        publisher_name = COALESCE(%s, publisher_name),
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s AND is_deleted = FALSE
                    RETURNING
                        id,
                        news_code,
                        news_title,
                        news_content,
                        news_type,
                        publisher_user_id,
                        publisher_username,
                        publisher_name,
                        reviewer_user_id,
                        reviewer_username,
                        reviewer_name,
                        published_at,
                        status,
                        is_pinned,
                        display_order,
                        created_at,
                        updated_at
                    """,
                    (
                        publisher_username,
                        publisher_name,
                        int(news_article_id),
                    ),
                )
                row = cur.fetchone()
                if row is None:
                    raise KeyError(news_article_id)
                record = self._normalize_news_row(dict(row))
            conn.commit()
        return record

    def offline_news_article(self, news_article_id: int) -> dict[str, Any]:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE dtlms_news_articles
                    SET status = '已下线',
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s AND is_deleted = FALSE
                    RETURNING
                        id,
                        news_code,
                        news_title,
                        news_content,
                        news_type,
                        publisher_user_id,
                        publisher_username,
                        publisher_name,
                        reviewer_user_id,
                        reviewer_username,
                        reviewer_name,
                        published_at,
                        status,
                        is_pinned,
                        display_order,
                        created_at,
                        updated_at
                    """,
                    (int(news_article_id),),
                )
                row = cur.fetchone()
                if row is None:
                    raise KeyError(news_article_id)
                record = self._normalize_news_row(dict(row))
            conn.commit()
        return record

    def batch_publish_news_articles(
        self,
        news_article_ids: list[int],
        *,
        publisher_username: str | None = None,
        publisher_name: str | None = None,
    ) -> int:
        self.ensure_schema()
        normalized_ids = [int(news_article_id) for news_article_id in news_article_ids if int(news_article_id) > 0]
        if not normalized_ids:
            return 0
        with self._connect(settings.postgres_db) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE dtlms_news_articles
                    SET status = '已发布',
                        published_at = COALESCE(published_at, CURRENT_TIMESTAMP),
                        publisher_username = COALESCE(%s, publisher_username),
                        publisher_name = COALESCE(%s, publisher_name),
                        updated_at = CURRENT_TIMESTAMP
                    WHERE is_deleted = FALSE AND id = ANY(%s)
                    """,
                    (
                        publisher_username,
                        publisher_name,
                        normalized_ids,
                    ),
                )
                success_count = int(cur.rowcount or 0)
            conn.commit()
        return success_count

    def batch_offline_news_articles(self, news_article_ids: list[int]) -> int:
        self.ensure_schema()
        normalized_ids = [int(news_article_id) for news_article_id in news_article_ids if int(news_article_id) > 0]
        if not normalized_ids:
            return 0
        with self._connect(settings.postgres_db) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE dtlms_news_articles
                    SET status = '已下线',
                        updated_at = CURRENT_TIMESTAMP
                    WHERE is_deleted = FALSE AND id = ANY(%s)
                    """,
                    (normalized_ids,),
                )
                success_count = int(cur.rowcount or 0)
            conn.commit()
        return success_count

    def list_dict_options(self, dict_type: str) -> list[dict[str, Any]]:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT label, value, color_type, css_class
                    FROM dtlms_dict_data
                    WHERE is_deleted = FALSE AND status = '启用' AND dict_type = %s
                    ORDER BY sort_order ASC, id ASC
                    """,
                    (dict_type,),
                )
                return [self._normalize_dict_row(dict(row)) for row in cur.fetchall()]

    def create_dict_type(self, payload: dict[str, Any]) -> dict[str, Any]:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM dtlms_dict_types WHERE is_deleted = FALSE AND dict_type = %s", (payload["dict_type"],))
                if cur.fetchone():
                    raise ValueError("Dict type already exists")
                cur.execute(
                    """
                    INSERT INTO dtlms_dict_types (dict_name, dict_type, status, remark)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id, dict_name, dict_type, status, remark
                    """,
                    (payload["dict_name"], payload["dict_type"], payload["status"], payload.get("remark")),
                )
                record = self._normalize_dict_row(self._require_row(cur.fetchone(), "create_dict_type"))
            conn.commit()
        return record | {"data_count": 0}

    def update_dict_type(self, dict_type_id: int, payload: dict[str, Any]) -> dict[str, Any]:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute("SELECT id, dict_type FROM dtlms_dict_types WHERE id = %s AND is_deleted = FALSE", (dict_type_id,))
                current = cur.fetchone()
                if not current:
                    raise KeyError(dict_type_id)
                cur.execute(
                    "SELECT id FROM dtlms_dict_types WHERE is_deleted = FALSE AND dict_type = %s AND id <> %s",
                    (payload["dict_type"], dict_type_id),
                )
                if cur.fetchone():
                    raise ValueError("Dict type already exists")
                cur.execute(
                    """
                    UPDATE dtlms_dict_types
                    SET dict_name = %s, dict_type = %s, status = %s, remark = %s, updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                    RETURNING id, dict_name, dict_type, status, remark
                    """,
                    (payload["dict_name"], payload["dict_type"], payload["status"], payload.get("remark"), dict_type_id),
                )
                record = self._normalize_dict_row(self._require_row(cur.fetchone(), "update_dict_type"))
                if current["dict_type"] != payload["dict_type"]:
                    cur.execute(
                        "UPDATE dtlms_dict_data SET dict_type = %s, updated_at = CURRENT_TIMESTAMP WHERE dict_type_id = %s AND is_deleted = FALSE",
                        (payload["dict_type"], dict_type_id),
                    )
                cur.execute("SELECT COUNT(*) AS count FROM dtlms_dict_data WHERE dict_type_id = %s AND is_deleted = FALSE", (dict_type_id,))
                count_row = cur.fetchone()
            conn.commit()
        return record | {"data_count": int(self._require_row(count_row, "update_dict_type_count")["count"])}

    def delete_dict_type(self, dict_type_id: int) -> None:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM dtlms_dict_types WHERE id = %s AND is_deleted = FALSE", (dict_type_id,))
                if not cur.fetchone():
                    raise KeyError(dict_type_id)
                cur.execute("SELECT COUNT(*) FROM dtlms_dict_data WHERE dict_type_id = %s AND is_deleted = FALSE", (dict_type_id,))
                if int(self._require_scalar_row(cur.fetchone(), "delete_dict_type_count")[0]) > 0:
                    raise ValueError("Dict type still has dict data")
                cur.execute("UPDATE dtlms_dict_types SET is_deleted = TRUE, updated_at = CURRENT_TIMESTAMP WHERE id = %s", (dict_type_id,))
            conn.commit()

    def create_dict_data(self, payload: dict[str, Any]) -> dict[str, Any]:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id, dict_name FROM dtlms_dict_types WHERE dict_type = %s AND is_deleted = FALSE",
                    (payload["dict_type"],),
                )
                dict_type_row = cur.fetchone()
                if not dict_type_row:
                    raise ValueError("Dict type does not exist")
                cur.execute(
                    "SELECT id FROM dtlms_dict_data WHERE dict_type = %s AND value = %s AND is_deleted = FALSE",
                    (payload["dict_type"], payload["value"]),
                )
                if cur.fetchone():
                    raise ValueError("Dict value already exists")
                cur.execute(
                    """
                    INSERT INTO dtlms_dict_data (dict_type_id, dict_type, label, value, sort_order, status, color_type, css_class, remark)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id, dict_type, label, value, sort_order, status, color_type, css_class, remark
                    """,
                    (
                        int(dict_type_row["id"]),
                        payload["dict_type"],
                        payload["label"],
                        payload["value"],
                        int(payload.get("sort_order", 0)),
                        payload["status"],
                        payload.get("color_type"),
                        payload.get("css_class"),
                        payload.get("remark"),
                    ),
                )
                record = self._normalize_dict_row(self._require_row(cur.fetchone(), "create_dict_data"))
            conn.commit()
        return record | {"dict_name": dict_type_row["dict_name"]}

    def update_dict_data(self, dict_data_id: int, payload: dict[str, Any]) -> dict[str, Any]:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM dtlms_dict_data WHERE id = %s AND is_deleted = FALSE", (dict_data_id,))
                if not cur.fetchone():
                    raise KeyError(dict_data_id)
                cur.execute(
                    "SELECT id, dict_name FROM dtlms_dict_types WHERE dict_type = %s AND is_deleted = FALSE",
                    (payload["dict_type"],),
                )
                dict_type_row = cur.fetchone()
                if not dict_type_row:
                    raise ValueError("Dict type does not exist")
                cur.execute(
                    "SELECT id FROM dtlms_dict_data WHERE dict_type = %s AND value = %s AND is_deleted = FALSE AND id <> %s",
                    (payload["dict_type"], payload["value"], dict_data_id),
                )
                if cur.fetchone():
                    raise ValueError("Dict value already exists")
                cur.execute(
                    """
                    UPDATE dtlms_dict_data
                    SET dict_type_id = %s,
                        dict_type = %s,
                        label = %s,
                        value = %s,
                        sort_order = %s,
                        status = %s,
                        color_type = %s,
                        css_class = %s,
                        remark = %s,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                    RETURNING id, dict_type, label, value, sort_order, status, color_type, css_class, remark
                    """,
                    (
                        int(dict_type_row["id"]),
                        payload["dict_type"],
                        payload["label"],
                        payload["value"],
                        int(payload.get("sort_order", 0)),
                        payload["status"],
                        payload.get("color_type"),
                        payload.get("css_class"),
                        payload.get("remark"),
                        dict_data_id,
                    ),
                )
                record = self._normalize_dict_row(self._require_row(cur.fetchone(), "update_dict_data"))
            conn.commit()
        return record | {"dict_name": dict_type_row["dict_name"]}

    @staticmethod
    def _normalize_dict_row(row: dict[str, Any]) -> dict[str, Any]:
        normalized: dict[str, Any] = {}
        for key, value in row.items():
            if isinstance(value, str):
                normalized[key] = value.strip()
            else:
                normalized[key] = value
        return normalized

    @staticmethod
    def _normalize_news_row(row: dict[str, Any]) -> dict[str, Any]:
        normalized: dict[str, Any] = {}
        for key, value in row.items():
            if isinstance(value, str):
                normalized[key] = value.strip()
            else:
                normalized[key] = value
        return normalized

    def delete_dict_data(self, dict_data_id: int) -> None:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM dtlms_dict_data WHERE id = %s AND is_deleted = FALSE", (dict_data_id,))
                if not cur.fetchone():
                    raise KeyError(dict_data_id)
                cur.execute("UPDATE dtlms_dict_data SET is_deleted = TRUE, updated_at = CURRENT_TIMESTAMP WHERE id = %s", (dict_data_id,))
            conn.commit()
