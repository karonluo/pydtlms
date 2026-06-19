from __future__ import annotations

from datetime import date, datetime
from typing import TYPE_CHECKING
from uuid import uuid4

from psycopg.rows import dict_row

from app.core.config import settings

from .management_service_shared import *


class RuntimeManagementStoreResearchCenterMixin:
    if TYPE_CHECKING:
        def __getattr__(self, name: str) -> Any: ...

    @staticmethod
    def _normalize_center_date(value: str | None) -> date | None:
        if not value:
            return None
        text = str(value).strip()
        if not text:
            return None
        try:
            return datetime.fromisoformat(text).date()
        except ValueError:
            try:
                return datetime.strptime(text, "%Y-%m-%d").date()
            except ValueError:
                return None

    @staticmethod
    def _normalize_center_status(is_enabled: bool | None) -> str:
        return "active" if is_enabled is not False else "inactive"

    @staticmethod
    def _normalize_text(value: Any, default: str = "") -> str:
        text = str(value or "").strip()
        return text or default

    @staticmethod
    def _normalize_int_list(values: Any) -> list[int]:
        normalized: list[int] = []
        for value in values or []:
            try:
                integer_value = int(value)
            except (TypeError, ValueError):
                continue
            if integer_value > 0:
                normalized.append(integer_value)
        return normalized

    def _build_center_record(self, row: dict[str, Any], *, member_student_count: int = 0, active_student_count: int = 0, student_count: int = 0) -> CenterRecord:
        lead_user_id = int(row.get("lead_user_id") or 0) or None
        # Read multi-director from row.directors / row.director_ids; fall back to lead_user_id.
        _directors_raw = row.get("directors") or []
        directors: list[CenterDirector] = []
        for _item in _directors_raw:
            if not _item:
                continue
            if isinstance(_item, dict):
                _uid = int(_item.get("user_id") or _item.get("id") or 0) or 0
                _fname = self._normalize_text(_item.get("full_name"))
                if _uid > 0 and _fname:
                    directors.append(CenterDirector(user_id=_uid, full_name=_fname))
            elif isinstance(_item, (list, tuple)) and len(_item) >= 2:
                _uid = int(_item[0] or 0) or 0
                _fname = self._normalize_text(_item[1])
                if _uid > 0 and _fname:
                    directors.append(CenterDirector(user_id=_uid, full_name=_fname))
        director_ids: list[int] = [int(v) for v in (row.get("director_ids") or []) if int(v or 0) > 0]
        lead_user_name = self._normalize_text(row.get("lead_user_name"))
        if not directors and lead_user_id is not None:
            # Fallback: synthesize one director from lead_user_id if no dtlms_team_leaders data.
            if not lead_user_name:
                lead_user_name = self._center_user_name_by_id(lead_user_id) or ""
            if lead_user_name:
                directors.append(CenterDirector(user_id=lead_user_id, full_name=lead_user_name))
                if lead_user_id not in director_ids:
                    director_ids.insert(0, lead_user_id)
        if directors:
            director_name = "、".join(d.full_name for d in directors)
            if lead_user_id is None:
                lead_user_id = directors[0].user_id
        elif lead_user_name:
            director_name = lead_user_name
        else:
            director_name = ""
        advisor_names = [self._normalize_text(item) for item in (row.get("advisor_names") or []) if self._normalize_text(item)]
        advisor_ids = [int(item) for item in (row.get("advisor_ids") or []) if int(item or 0) > 0]
        advisor_relation_ids = [int(item) for item in (row.get("advisor_relation_ids") or []) if int(item or 0) > 0]
        return CenterRecord(
            id=int(row.get("id") or 0),
            center_name=self._normalize_text(row.get("team_name")),
            director_name=director_name,
            director_id=lead_user_id,
            director_ids=director_ids,
            directors=directors,
            advisor_names=advisor_names,
            advisor_ids=advisor_ids,
            advisor_relation_ids=advisor_relation_ids,
            is_enabled=str(row.get("team_status") or "").strip() == "active",
            created_date=self._normalize_optional_text(row.get("created_date") or row.get("established_on") or row.get("created_at")),
            member_student_count=member_student_count,
            active_student_count=active_student_count,
            student_count=student_count,
        )

    @staticmethod
    def _normalize_optional_text(value: Any) -> str | None:
        text = str(value or "").strip()
        return text or None

    def _ensure_center_schema(self) -> None:
        ensure_schema = getattr(self._postgres_store, "ensure_schema", None)
        if callable(ensure_schema):
            ensure_schema()

    def _center_store_uses_database(self) -> bool:
        return callable(getattr(self._postgres_store, "_connect", None))

    @staticmethod
    def _center_fake_team_payload(
        *,
        center_id: int,
        team_name: str,
        lead_user_id: int,
        team_status: str,
        established_on: date | None,
    ) -> dict[str, Any]:
        return {
            "id": int(center_id),
            "team_name": team_name,
            "department_name": "未分配院系",
            "discipline_name": None,
            "lead_user_id": int(lead_user_id),
            "team_status": team_status,
            "established_on": established_on,
            "description": None,
            "is_deleted": False,
        }

    def _center_user_name_by_id(self, user_id: int | None) -> str | None:
        if user_id is None:
            return None
        self._ensure_center_schema()
        with self._postgres_store._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT u.full_name
                    FROM dtlms_users u
                    JOIN dtlms_user_roles ur ON ur.user_id = u.id
                    JOIN dtlms_roles r ON r.id = ur.role_id AND r.is_deleted = FALSE
                    WHERE u.id = %s
                      AND u.is_deleted = FALSE
                      AND r.role_code = 'advisor'
                    LIMIT 1
                    """,
                    (int(user_id),),
                )
                row = cur.fetchone()
                return self._normalize_text(row.get("full_name")) if row else None

    def get_centers(
        self,
        keyword: str | None = None,
        is_enabled: bool | None = None,
        # 旧入参 director_id（单值）保留以兼容老调用方，新代码请使用 director_ids（多值）
        director_id: int | None = None,
        director_ids: list[int] | None = None,
        principal: Principal | dict[str, Any] | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> CenterListResponse:
        # 兼容合并 director_id + director_ids
        _merged_director_ids: list[int] = list(director_ids or [])
        if director_id and int(director_id) not in _merged_director_ids:
            _merged_director_ids.append(int(director_id))
        _effective_director_ids: list[int] | None = _merged_director_ids or None

        self._ensure_center_schema()
        if not self._center_store_uses_database():
            list_centers_page = getattr(self._postgres_store, "list_centers_page", None)
            if callable(list_centers_page):
                items, total = list_centers_page(
                    keyword=keyword,
                    is_enabled=is_enabled,
                    director_ids=_effective_director_ids,
                    page=page,
                    page_size=page_size,
                    principal=principal,
                )
                normalized_items = []
                for item in items:
                    row = dict(item)
                    normalized_items.append(
                        self._build_center_record(
                            {
                                **row,
                                "team_name": row.get("team_name") or row.get("center_name"),
                                "lead_user_name": row.get("lead_user_name") or row.get("director_name"),
                                "lead_user_id": row.get("lead_user_id") or row.get("director_id"),
                            },
                            member_student_count=int(row.get("member_student_count") or 0),
                            active_student_count=int(row.get("active_student_count") or 0),
                            student_count=int(row.get("student_count") or 0),
                        )
                    )
                return CenterListResponse(items=normalized_items, total=int(total or 0), page=page, page_size=page_size)
            return CenterListResponse(items=[], total=0, page=page, page_size=page_size)

        offset = max(page - 1, 0) * page_size
        where_clauses = ["t.is_deleted = FALSE"]
        params: list[Any] = []

        if keyword and str(keyword).strip():
            keyword_like = f"%{str(keyword).strip()}%"
            where_clauses.append(
                """
                (
                    t.team_name ILIKE %s
                    OR COALESCE(t.department_name, '') ILIKE %s
                    OR COALESCE(t.discipline_name, '') ILIKE %s
                    OR COALESCE(t.description, '') ILIKE %s
                )
                """
            )
            params.extend([keyword_like] * 4)
        if is_enabled is not None:
            where_clauses.append("t.team_status = %s" if is_enabled else "t.team_status <> %s")
            params.append("active")
        if _effective_director_ids:
            where_clauses.append(
                "EXISTS (SELECT 1 FROM dtlms_team_leaders tl_scope WHERE tl_scope.team_id = t.id AND tl_scope.user_id = ANY(%s))"
            )
            params.append(list(_effective_director_ids))
        # Mirror the postgres path's advisor scope filter so an advisor only
        # sees centers they lead or belong to. "Lead" now means appearing in
        # dtlms_team_leaders (multi-value), not the legacy dtlms_teams.lead_user_id.
        _role_codes = set()
        if principal is not None:
            _raw_roles = getattr(principal, "roles", None)
            if _raw_roles is None and isinstance(principal, dict):
                _raw_roles = principal.get("roles") or []
            _role_codes = {str(item).strip() for item in (_raw_roles or []) if str(item).strip()}
        _bypass_roles = {"platform_admin", "AILABMGT", "academy_admin"}
        if _role_codes and not (_role_codes & _bypass_roles) and "advisor" in _role_codes:
            _username = str(getattr(principal, "username", "") or "").strip()
            if not _username and isinstance(principal, dict):
                _username = str(principal.get("username") or "").strip()
            if not _username:
                return CenterListResponse(items=[], total=0, page=page, page_size=page_size)
            where_clauses.append(
                """
                (
                    EXISTS (
                        SELECT 1 FROM dtlms_team_leaders tl_scope
                        JOIN dtlms_users lead_user_scope
                          ON lead_user_scope.id = tl_scope.user_id
                         AND lead_user_scope.is_deleted = FALSE
                        WHERE tl_scope.team_id = t.id
                          AND lead_user_scope.username = %s
                    )
                    OR EXISTS (
                        SELECT 1 FROM dtlms_team_advisors ta_scope
                        JOIN dtlms_users advisor_scope
                          ON advisor_scope.id = ta_scope.advisor_user_id
                         AND advisor_scope.is_deleted = FALSE
                        WHERE ta_scope.team_id = t.id
                          AND ta_scope.is_deleted = FALSE
                          AND advisor_scope.username = %s
                    )
                )
                """
            )
            params.extend([_username, _username])

        where_sql = " AND ".join(where_clauses)
        with self._postgres_store._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    f"""
                    SELECT COUNT(*) AS total
                    FROM dtlms_teams t
                    WHERE {where_sql}
                    """,
                    params,
                )
                total_row = cur.fetchone()
                total = int(total_row["total"] if total_row else 0)

                cur.execute(
                    f"""
                    SELECT
                        t.id,
                        t.team_name,
                        t.lead_user_id,
                        lead_user.full_name AS lead_user_name,
                        COALESCE(team_leaders.director_ids, ARRAY[]::bigint[]) AS director_ids,
                        COALESCE(team_leaders.directors_json, '[]'::jsonb) AS directors,
                        COALESCE(advisor_rows.advisor_names, ARRAY[]::text[]) AS advisor_names,
                        COALESCE(advisor_rows.advisor_names_arr, ARRAY[]::text[]) AS advisor_names_arr,
                        COALESCE(advisor_rows.advisor_ids, ARRAY[]::bigint[]) AS advisor_ids,
                        COALESCE(advisor_rows.advisor_relation_ids, ARRAY[]::bigint[]) AS advisor_relation_ids,
                        t.team_status,
                        COALESCE(TO_CHAR(t.established_on, 'YYYY-MM-DD'), TO_CHAR(t.created_at::date, 'YYYY-MM-DD')) AS created_date,
                        COALESCE(student_stats.member_student_count, 0) AS member_student_count,
                        COALESCE(student_stats.active_student_count, 0) AS active_student_count,
                        COALESCE(student_stats.student_count, 0) AS student_count
                    FROM dtlms_teams t
                    LEFT JOIN dtlms_users lead_user
                      ON lead_user.id = t.lead_user_id
                     AND lead_user.is_deleted = FALSE
                                        LEFT JOIN LATERAL (
                                                SELECT
                                                        array_agg(DISTINCT advisor_user.full_name ORDER BY advisor_user.full_name) AS advisor_names,
                                                        array_agg(DISTINCT advisor_user.full_name ORDER BY advisor_user.full_name) AS advisor_names_arr,
                                                        array_agg(DISTINCT ta.advisor_user_id ORDER BY ta.advisor_user_id) AS advisor_ids,
                                                        array_agg(DISTINCT ta.id ORDER BY ta.id) AS advisor_relation_ids
                                                FROM dtlms_team_advisors ta
                                                JOIN dtlms_users advisor_user
                                                    ON advisor_user.id = ta.advisor_user_id
                                                 AND advisor_user.is_deleted = FALSE
                                                JOIN dtlms_user_roles ur
                                                    ON ur.user_id = advisor_user.id
                                                JOIN dtlms_roles r
                                                    ON r.id = ur.role_id
                                                 AND r.is_deleted = FALSE
                                                WHERE ta.team_id = t.id
                                                    AND ta.is_deleted = FALSE
                                                    AND r.role_code = 'advisor'
                                        ) advisor_rows ON TRUE
                    LEFT JOIN LATERAL (
                        SELECT
                            array_agg(tl.user_id ORDER BY u.full_name, tl.user_id) AS director_ids,
                            COALESCE(jsonb_agg(jsonb_build_object('user_id', tl.user_id, 'full_name', u.full_name) ORDER BY u.full_name, tl.user_id), '[]'::jsonb) AS directors_json
                        FROM dtlms_team_leaders tl
                        JOIN dtlms_users u ON u.id = tl.user_id AND u.is_deleted = FALSE
                        WHERE tl.team_id = t.id
                    ) team_leaders ON TRUE
                    LEFT JOIN LATERAL (
                        SELECT
                            COUNT(*) AS member_student_count,
                            COUNT(*) FILTER (WHERE s.current_status IN ('enrolled', 'internship', 'outbound', 'thesis')) AS active_student_count,
                            (
                                SELECT COUNT(DISTINCT offer.candidate_no)
                                FROM dtlms_plan_offer offer
                                JOIN dtlms_recruitment_applications app
                                    ON app.candidate_no = offer.candidate_no
                                       AND app.is_deleted = FALSE
                                WHERE offer.submitted_at IS NOT NULL
                                  AND offer.is_agree = TRUE
                                  AND (
                                        (app.first_choice_screening_score >= 80
                                            AND app.first_choice = ANY (advisor_rows.advisor_names_arr))
                                     OR (app.second_choice_screening_score >= 80
                                            AND app.second_choice = ANY (advisor_rows.advisor_names_arr))
                                  )
                            ) AS student_count
                        FROM dtlms_students s
                        WHERE s.team_id = t.id AND s.is_deleted = FALSE
                    ) student_stats ON TRUE
                    WHERE {where_sql}
                    ORDER BY t.id DESC
                    LIMIT %s OFFSET %s
                    """,
                    [*params, page_size, offset],
                )
                items = []
                for row in cur.fetchall():
                    items.append(
                        self._build_center_record(
                            dict(row),
                            member_student_count=int(row.get("member_student_count") or 0),
                            active_student_count=int(row.get("active_student_count") or 0),
                            student_count=int(row.get("student_count") or 0),
                        )
                    )
                return CenterListResponse(items=items, total=total, page=page, page_size=page_size)

    def create_center(self, payload: CenterUpsert) -> CenterRecord:
        self._ensure_center_schema()
        if not self._center_store_uses_database():
            team_name = self._normalize_text(payload.center_name)
            if not team_name:
                raise ValueError("中心名称不能为空")
            lead_user_id = int(payload.director_id or 0) or 1
            established_on = self._normalize_center_date(payload.created_date)
            created_centers = getattr(self._postgres_store, "created_centers", None)
            center_id = len(created_centers or []) + 1
            team_payload = self._center_fake_team_payload(
                center_id=center_id,
                team_name=team_name,
                lead_user_id=lead_user_id,
                team_status=self._normalize_center_status(payload.is_enabled),
                established_on=established_on,
            )
            sync_created_center = getattr(self._postgres_store, "sync_created_center", None)
            if callable(sync_created_center):
                sync_created_center(team_payload, None, None)
            return self._build_center_record(
                {
                    **team_payload,
                    "lead_user_name": self._normalize_text(payload.director_name),
                    "advisor_names": self._normalize_int_list(payload.advisor_ids),
                    "advisor_ids": self._normalize_int_list(payload.advisor_ids),
                    "advisor_relation_ids": [],
                    "created_date": established_on.isoformat() if established_on else None,
                }
            )

        with self._postgres_store._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                team_name = self._normalize_text(payload.center_name)
                if not team_name:
                    raise ValueError("中心名称不能为空")
                established_on = self._normalize_center_date(payload.created_date)
                # 优先从 director_ids（多值）取负责人；向后兼容 director_id / director_name
                director_user_ids: list[int] = []
                for item in (payload.director_ids or []):
                    try:
                        integer = int(item)
                    except (TypeError, ValueError):
                        continue
                    if integer > 0 and integer not in director_user_ids:
                        director_user_ids.append(integer)
                if not director_user_ids and payload.director_id:
                    try:
                        director_user_ids.append(int(payload.director_id))
                    except (TypeError, ValueError):
                        pass
                lead_user_id: int | None = director_user_ids[0] if director_user_ids else None
                lead_user_name = self._normalize_text(payload.director_name)
                if lead_user_id is None and lead_user_name:
                    lead_user_id = self._resolve_advisor_user_id_by_name(lead_user_name)
                if lead_user_id is None:
                    raise ValueError("请选择导师角色用户作为负责人")
                advisor_user_ids = self._normalize_int_list(payload.advisor_ids)
                if lead_user_id not in advisor_user_ids:
                    advisor_user_ids.insert(0, lead_user_id)
                team_code = f"CENTER-{uuid4().hex[:12].upper()}"
                # Sync dtlms_teams_id_seq with MAX(id) to avoid UniqueViolation on physically-deleted IDs.
                cur.execute(
                    "SELECT setval('dtlms_teams_id_seq', COALESCE((SELECT MAX(id) FROM dtlms_teams), 1), true)",
                )
                cur.execute(
                    """
                    INSERT INTO dtlms_teams (
                        team_code,
                        team_name,
                        department_name,
                        discipline_name,
                        lead_user_id,
                        team_status,
                        established_on,
                        description,
                        is_deleted
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, FALSE)
                    RETURNING id
                    """,
                    (
                        team_code,
                        team_name,
                        "未分配院系",
                        None,
                        lead_user_id,
                        self._normalize_center_status(payload.is_enabled),
                        established_on,
                        None,
                    ),
                )
                team_row = dict(cur.fetchone() or {})
                team_id = int(team_row.get("id") or 0)
                self._sync_center_advisor_relations(cur, team_id, advisor_user_ids)
                self._sync_center_leaders(cur, team_id, director_user_ids)
                row = self._load_center_row(cur, team_id)
            conn.commit()
        return self._build_center_record(row)

    def update_center(self, center_id: int, payload: CenterUpsert) -> CenterRecord:
        self._ensure_center_schema()
        if not self._center_store_uses_database():
            team_name = self._normalize_text(payload.center_name)
            if not team_name:
                raise ValueError("中心名称不能为空")
            lead_user_id = int(payload.director_id or 0) or 1
            established_on = self._normalize_center_date(payload.created_date)
            team_payload = self._center_fake_team_payload(
                center_id=int(center_id),
                team_name=team_name,
                lead_user_id=lead_user_id,
                team_status=self._normalize_center_status(payload.is_enabled),
                established_on=established_on,
            )
            sync_updated_center = getattr(self._postgres_store, "sync_updated_center", None)
            try:
                if callable(sync_updated_center):
                    sync_updated_center(team_payload, [], None, None)
            except Exception:
                save_state = getattr(self, "_save", None)
                if callable(save_state):
                    save_state()
            return self._build_center_record(
                {
                    **team_payload,
                    "lead_user_name": self._normalize_text(payload.director_name),
                    "advisor_names": self._normalize_int_list(payload.advisor_ids),
                    "advisor_ids": self._normalize_int_list(payload.advisor_ids),
                    "advisor_relation_ids": [],
                    "created_date": established_on.isoformat() if established_on else None,
                }
            )

        with self._postgres_store._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                current_row = self._load_center_row(cur, int(center_id))
                if current_row is None:
                    raise KeyError(center_id)

                team_name = self._normalize_text(payload.center_name)
                if not team_name:
                    raise ValueError("中心名称不能为空")
                established_on = self._normalize_center_date(payload.created_date)
                # 优先从 director_ids（多值）取负责人；向后兼容 director_id / director_name
                director_user_ids: list[int] = []
                for item in (payload.director_ids or []):
                    try:
                        integer = int(item)
                    except (TypeError, ValueError):
                        continue
                    if integer > 0 and integer not in director_user_ids:
                        director_user_ids.append(integer)
                if not director_user_ids and payload.director_id:
                    try:
                        director_user_ids.append(int(payload.director_id))
                    except (TypeError, ValueError):
                        pass
                lead_user_id: int | None = director_user_ids[0] if director_user_ids else None
                lead_user_name = self._normalize_text(payload.director_name)
                if lead_user_id is None and lead_user_name:
                    lead_user_id = self._resolve_advisor_user_id_by_name(lead_user_name)
                if lead_user_id is None:
                    raise ValueError("请选择导师角色用户作为负责人")
                advisor_user_ids = self._normalize_int_list(payload.advisor_ids)
                if lead_user_id not in advisor_user_ids:
                    advisor_user_ids.insert(0, lead_user_id)
                cur.execute(
                    """
                    UPDATE dtlms_teams
                    SET team_name = %s,
                        department_name = %s,
                        discipline_name = %s,
                        lead_user_id = %s,
                        team_status = %s,
                        established_on = %s,
                        description = %s,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                    RETURNING id, team_name, department_name, discipline_name, lead_user_id, team_status, established_on, description, created_at
                    """,
                    (
                        team_name,
                        "未分配院系",
                        None,
                        lead_user_id,
                        self._normalize_center_status(payload.is_enabled),
                        established_on,
                        None,
                        int(center_id),
                    ),
                )
                self._sync_center_advisor_relations(cur, int(center_id), advisor_user_ids)
                self._sync_center_leaders(cur, int(center_id), director_user_ids)
                row = self._load_center_row(cur, int(center_id)) or dict(cur.fetchone() or {})
            conn.commit()
        return self._build_center_record(row)

    def delete_center(self, center_id: int) -> None:
        self._ensure_center_schema()
        if not self._center_store_uses_database():
            sync_deleted_center = getattr(self._postgres_store, "sync_deleted_center", None)
            if callable(sync_deleted_center):
                sync_deleted_center(int(center_id), None, None)
            return

        with self._postgres_store._connect(settings.postgres_db) as conn:
            with conn.cursor() as cur:
                # Physical delete: drop related rows first, then the team row.
                cur.execute(
                    """
                    DELETE FROM dtlms_team_leaders
                    WHERE team_id = %s
                    """
                    ,
                    (int(center_id),),
                )
                cur.execute(
                    """
                    DELETE FROM dtlms_team_advisors
                    WHERE team_id = %s
                    """
                    ,
                    (int(center_id),),
                )
                cur.execute(
                    """
                    DELETE FROM dtlms_teams
                    WHERE id = %s
                    """
                    ,
                    (int(center_id),),
                )
                if cur.rowcount <= 0:
                    raise KeyError(center_id)
            conn.commit()

    def delete_centers(self, center_ids: list[int]) -> BulkActionResponse:
        success_count = 0
        for center_id in center_ids:
            self.delete_center(int(center_id))
            success_count += 1
        return BulkActionResponse(success_count=success_count)

    def _load_center_row(self, cur: Any, center_id: int) -> dict[str, Any] | None:
        cur.execute(
            """
            SELECT
                t.id,
                t.team_name,
                t.department_name,
                t.discipline_name,
                t.lead_user_id,
                lead_user.full_name AS lead_user_name,
                t.team_status,
                t.established_on,
                t.description,
                t.created_at,
                COALESCE(team_leaders.director_ids, ARRAY[]::bigint[]) AS director_ids,
                COALESCE(team_leaders.directors_json, '[]'::jsonb) AS directors
            FROM dtlms_teams t
            LEFT JOIN dtlms_users lead_user
              ON lead_user.id = t.lead_user_id
             AND lead_user.is_deleted = FALSE
            LEFT JOIN LATERAL (
                SELECT
                    array_agg(tl.user_id ORDER BY u.full_name, tl.user_id) AS director_ids,
                    COALESCE(jsonb_agg(jsonb_build_object('user_id', tl.user_id, 'full_name', u.full_name) ORDER BY u.full_name, tl.user_id), '[]'::jsonb) AS directors_json
                FROM dtlms_team_leaders tl
                JOIN dtlms_users u ON u.id = tl.user_id AND u.is_deleted = FALSE
                WHERE tl.team_id = t.id
            ) team_leaders ON TRUE
            WHERE t.id = %s
              AND t.is_deleted = FALSE
            """,
            (int(center_id),),
        )
        row = cur.fetchone()
        return dict(row) if row else None

    def _resolve_advisor_user_id_by_name(self, full_name: str) -> int | None:
        normalized_name = self._normalize_text(full_name)
        if not normalized_name:
            return None
        self._ensure_center_schema()
        with self._postgres_store._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT u.id
                    FROM dtlms_users u
                    JOIN dtlms_user_roles ur ON ur.user_id = u.id
                    JOIN dtlms_roles r ON r.id = ur.role_id AND r.is_deleted = FALSE
                    WHERE u.full_name = %s
                      AND u.is_deleted = FALSE
                      AND r.role_code = 'advisor'
                    ORDER BY u.id
                    LIMIT 1
                    """,
                    (normalized_name,),
                )
                row = cur.fetchone()
                return int(row[0]) if row else None

    def _sync_center_leaders(self, cur: Any, center_id: int, director_user_ids: list[int]) -> None:
        # Sync director_ids into dtlms_team_leaders (delete then insert, ON CONFLICT DO NOTHING).
        try:
            cur.execute(
                """
                DELETE FROM dtlms_team_leaders WHERE team_id = %s
                """,
                (int(center_id),),
            )
        except Exception as exc:
            logger.warning("dtlms_team_leaders DELETE skipped: %s", exc)
            return
        unique: list[int] = []
        seen: set[int] = set()
        for item in director_user_ids or []:
            try:
                integer = int(item)
            except (TypeError, ValueError):
                continue
            if integer <= 0 or integer in seen:
                continue
            seen.add(integer)
            unique.append(integer)
        for user_id in unique:
            try:
                cur.execute(
                    """
                    INSERT INTO dtlms_team_leaders (team_id, user_id)
                    VALUES (%s, %s)
                    ON CONFLICT (team_id, user_id) DO NOTHING
                    """,
                    (int(center_id), int(user_id)),
                )
            except Exception as exc:
                logger.warning("dtlms_team_leaders INSERT failed (team_id=%s, user_id=%s): %s", center_id, user_id, exc)

    def _sync_center_advisor_relations(self, cur: Any, center_id: int, advisor_user_ids: list[int]) -> None:
        cur.execute(
            """
            DELETE FROM dtlms_team_advisors
            WHERE team_id = %s
            """,
            (int(center_id),),
        )
        if not advisor_user_ids:
            return
        for advisor_user_id in dict.fromkeys(int(item) for item in advisor_user_ids if int(item or 0) > 0):
            cur.execute(
                """
                INSERT INTO dtlms_team_advisors (
                    team_id,
                    advisor_user_id,
                    is_deleted
                ) VALUES (%s, %s, FALSE)
                """,
                (int(center_id), int(advisor_user_id)),
            )


def get_center_list(
    keyword: str | None = None,
    is_enabled: bool | None = None,
    # 旧入参 director_id（单值）保留以兼容老调用方，新代码请使用 director_ids（多值）
    director_id: int | None = None,
    director_ids: list[int] | None = None,
    principal: Principal | dict[str, Any] | None = None,
    page: int = 1,
    page_size: int = 10,
) -> CenterListResponse:
    from .management_service import store

    # 兼容处理：director_id（单值）合并进 director_ids（多值）；director_ids 优先
    merged: list[int] = list(director_ids or [])
    if director_id and int(director_id) not in merged:
        merged.append(int(director_id))

    return store.get_centers(
        keyword=keyword,
        is_enabled=is_enabled,
        director_ids=merged or None,
        principal=principal,
        page=page,
        page_size=page_size,
    )


def create_center(payload: CenterUpsert) -> CenterRecord:
    from .management_service import store

    return store.create_center(payload)


def update_center(center_id: int, payload: CenterUpsert) -> CenterRecord:
    from .management_service import store

    return store.update_center(center_id, payload)


def delete_center(center_id: int) -> None:
    from .management_service import store

    store.delete_center(center_id)


def delete_centers(center_ids: list[int]) -> BulkActionResponse:
    from .management_service import store

    return store.delete_centers(center_ids)