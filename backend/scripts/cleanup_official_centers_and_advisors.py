from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from psycopg.rows import dict_row


BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


from app.core.config import settings


DEFAULT_PASSWORD_HASH = "$pbkdf2-sha256$29000$ESIkZKwVorQ2Ziyl9N77Xw$FkNpUi.BNeyqPLVId/t5Lz8zI0V1H7AbVTwDtfY.CNM"

TEAM_SPECS: list[dict[str, Any]] = [
    {
        "order": 1,
        "team_name": "前沿探索中心",
        "lead": "乔宇",
        "advisors": ["乔宇", "周伯文", "成宇", "石博天", "薛天帆", "蔡品隆", "邹娜", "刘翼豪", "何军军", "陈昕苑", "胡杨", "张超"],
    },
    {
        "order": 2,
        "team_name": "AI For Science中心",
        "lead": "白磊",
        "advisors": ["白磊", "周伯文", "欧阳万里", "张铂", "李玉强", "董楠卿", "宋纯锋", "胡舒悦", "王潚崧", "郝红霞"],
    },
    {
        "order": 3,
        "team_name": "大模型中心",
        "lead": "陈恺",
        "advisors": ["陈恺", "周伯文", "林达华", "王利民", "张文蔚", "郭琦鹏", "王毅", "李亦宁", "张超", "张奇"],
    },
    {
        "order": 4,
        "team_name": "物理智能中心",
        "lead": "张伟楠",
        "advisors": ["张伟楠", "周伯文", "沈春华", "翟少鹏", "赵斌", "吕照阳", "穆尧", "沈渊"],
    },
    {
        "order": 5,
        "team_name": "安全可信AI中心",
        "lead": "胡侠",
        "advisors": ["胡侠", "周伯文", "陆超超", "邵婧", "王迎春", "杨超", "滕妍", "瞿晶晶"],
    },
    {
        "order": 6,
        "team_name": "评测中心",
        "lead": "翟广涛",
        "advisors": ["翟广涛", "周伯文", "胡侠"],
    },
    {
        "order": 7,
        "team_name": "Data-CentricAI",
        "lead": "何聪辉",
        "advisors": ["何聪辉", "周伯文", "林达华", "王斌", "吴郦军", "吴江", "邱剑涛"],
    },
    {
        "order": 8,
        "team_name": "系统平台中心",
        "lead": "林达华",
        "advisors": ["林达华", "周伯文", "李恒杰"],
    },
]

USERNAME_MAP = {
    "乔宇": "qiaoyu",
    "周伯文": "zhoubowen",
    "成宇": "chengyu",
    "石博天": "shibotian",
    "薛天帆": "xuetianfan",
    "蔡品隆": "caipinlong",
    "邹娜": "zouna",
    "刘翼豪": "liuyihao",
    "何军军": "hejunjun",
    "陈昕苑": "chenxinyuan",
    "胡杨": "huyang",
    "张超": "zhangchao",
    "白磊": "bailei",
    "欧阳万里": "ouyangwanli",
    "张铂": "zhangbo",
    "李玉强": "liyuqiang",
    "董楠卿": "dongnanqing",
    "宋纯锋": "songchunfeng",
    "胡舒悦": "hushuyue",
    "王潚崧": "wangsusong",
    "郝红霞": "haohongxia",
    "陈恺": "chenkai",
    "林达华": "lindahua",
    "王利民": "wanglimin",
    "张文蔚": "zhangwenwei",
    "郭琦鹏": "guoqipeng",
    "王毅": "wangyi",
    "李亦宁": "liyining",
    "张奇": "zhangqi",
    "张伟楠": "zhangweinan",
    "沈春华": "shenchunhua",
    "翟少鹏": "dishaopeng",
    "赵斌": "zhaobin",
    "吕照阳": "lvzhaoyang",
    "穆尧": "muyao",
    "沈渊": "shenyuan",
    "胡侠": "huxia",
    "陆超超": "luchaochao",
    "邵婧": "shaojing",
    "王迎春": "wangyingchun",
    "杨超": "yangchao",
    "滕妍": "tengyan",
    "瞿晶晶": "qujingjing",
    "翟广涛": "diguangtao",
    "何聪辉": "heconghui",
    "王斌": "wangbin",
    "吴郦军": "wulijun",
    "吴江": "wujiang",
    "邱剑涛": "qiujiantao",
    "李恒杰": "lihengjie",
}

TEAM_ORDER = [item["team_name"] for item in TEAM_SPECS]
ALLOWED_TEAM_SET = set(TEAM_ORDER)
TEAM_TO_ADVISORS = {item["team_name"]: list(item["advisors"]) for item in TEAM_SPECS}
ALLOWED_ADVISOR_SET = {advisor for item in TEAM_SPECS for advisor in item["advisors"]}
ADVISOR_TO_TEAMS: dict[str, list[str]] = {}
for item in TEAM_SPECS:
    for advisor in item["advisors"]:
        ADVISOR_TO_TEAMS.setdefault(advisor, []).append(item["team_name"])


def normalize_text(value: Any) -> str:
    return str(value or "").strip()


def stable_pick(key: str, options: list[str]) -> str:
    if not options:
        raise ValueError("stable_pick options cannot be empty")
    ordered = list(options)
    digest = hashlib.sha256(key.encode("utf-8")).digest()
    index = int.from_bytes(digest[:8], "big") % len(ordered)
    return ordered[index]


def connect(*, autocommit: bool = False):
    import psycopg

    return psycopg.connect(
        host=settings.postgres_host,
        port=settings.postgres_port,
        dbname=settings.postgres_db,
        user=settings.postgres_user,
        password=settings.postgres_password,
        client_encoding="utf8",
        autocommit=autocommit,
    )


def fetch_scalar(cur, sql: str, params: tuple[Any, ...] = ()) -> Any:
    cur.execute(sql, params)
    row = cur.fetchone()
    return row[0] if row else None


def table_exists(cur, table_name: str) -> bool:
    return bool(
        fetch_scalar(
            cur,
            "SELECT 1 FROM information_schema.tables WHERE table_schema = 'public' AND table_name = %s",
            (table_name,),
        )
    )


def column_exists(cur, table_name: str, column_name: str) -> bool:
    return bool(
        fetch_scalar(
            cur,
            "SELECT 1 FROM information_schema.columns WHERE table_schema = 'public' AND table_name = %s AND column_name = %s",
            (table_name, column_name),
        )
    )


def build_advisor_metadata() -> dict[str, dict[str, str]]:
    metadata: dict[str, dict[str, str]] = {}
    for advisor_name, teams in ADVISOR_TO_TEAMS.items():
        lead_teams = [item["team_name"] for item in TEAM_SPECS if item["lead"] == advisor_name]
        if lead_teams:
            department_name = lead_teams[0]
        elif len(teams) == 1:
            department_name = teams[0]
        else:
            department_name = "多中心联合"
        metadata[advisor_name] = {
            "department_name": department_name,
            "research_direction": "、".join(teams),
        }
    return metadata


ADVISOR_METADATA = build_advisor_metadata()


def canonical_team_and_advisor(current_team: str, current_advisor: str, key: str, *, exclude_team: str | None = None) -> tuple[str, str]:
    team_name = normalize_text(current_team)
    advisor_name = normalize_text(current_advisor)

    if team_name in ALLOWED_TEAM_SET and team_name != exclude_team:
        resolved_team = team_name
    else:
        advisor_teams = [name for name in ADVISOR_TO_TEAMS.get(advisor_name, []) if name != exclude_team]
        if advisor_teams:
            resolved_team = stable_pick(f"{key}:team-from-advisor", advisor_teams)
        else:
            team_candidates = [name for name in TEAM_ORDER if name != exclude_team] or TEAM_ORDER
            resolved_team = stable_pick(f"{key}:team", team_candidates)

    team_advisors = TEAM_TO_ADVISORS[resolved_team]
    if advisor_name in team_advisors:
        resolved_advisor = advisor_name
    else:
        resolved_advisor = stable_pick(f"{key}:advisor", team_advisors)
    return resolved_team, resolved_advisor


def canonical_secondary_team(current_team: str, key: str, *, exclude_team: str) -> str:
    team_name = normalize_text(current_team)
    if team_name in ALLOWED_TEAM_SET and team_name != exclude_team:
        return team_name
    candidates = [name for name in TEAM_ORDER if name != exclude_team] or TEAM_ORDER
    return stable_pick(f"{key}:secondary-team", candidates)


def load_name_id_maps(cur) -> tuple[dict[str, int], dict[str, int]]:
    cur.execute("SELECT id, team_name FROM dtlms_teams WHERE is_deleted = FALSE")
    team_name_to_id = {normalize_text(name): team_id for team_id, name in cur.fetchall()}
    cur.execute("SELECT id, full_name FROM dtlms_advisors WHERE is_deleted = FALSE")
    advisor_name_to_id = {normalize_text(name): advisor_id for advisor_id, name in cur.fetchall()}
    return team_name_to_id, advisor_name_to_id


def ensure_advisors(cur, stats: dict[str, Any], *, apply_changes: bool) -> None:
    existing_names = set()
    cur.execute("SELECT full_name FROM dtlms_advisors")
    existing_names = {normalize_text(row[0]) for row in cur.fetchall()}

    max_no = fetch_scalar(
        cur,
        "SELECT COALESCE(MAX(CAST(SUBSTRING(advisor_no FROM 4) AS INTEGER)), 0) FROM dtlms_advisors WHERE advisor_no ~ '^ADV[0-9]+$'",
    ) or 0
    next_no = int(max_no)

    for advisor_name in sorted(ALLOWED_ADVISOR_SET):
        metadata = ADVISOR_METADATA[advisor_name]
        cur.execute(
            """
            UPDATE dtlms_advisors
            SET title = '导师',
                organization_name = %s,
                research_direction = %s,
                annual_quota = 0,
                is_deleted = FALSE,
                updated_at = CURRENT_TIMESTAMP
            WHERE full_name = %s
            """,
            (metadata["department_name"], metadata["research_direction"], advisor_name),
        )
        if cur.rowcount:
            stats["advisors_updated"] += cur.rowcount
            continue
        if apply_changes:
            next_no += 1
            advisor_no = f"ADV{next_no:03d}"
            cur.execute(
                """
                INSERT INTO dtlms_advisors (
                    advisor_no, full_name, title, organization_name, research_direction, annual_quota, is_deleted
                ) VALUES (%s, %s, '导师', %s, %s, 0, FALSE)
                """,
                (advisor_no, advisor_name, metadata["department_name"], metadata["research_direction"]),
            )
        stats["advisors_inserted"] += 1


def ensure_advisor_users(cur, stats: dict[str, Any]) -> None:
    if not table_exists(cur, "dtlms_users"):
        return
    role_id = fetch_scalar(cur, "SELECT id FROM dtlms_roles WHERE role_code = 'advisor' ORDER BY id LIMIT 1")
    if role_id is None:
        cur.execute(
            """
            INSERT INTO dtlms_roles (role_code, role_name, scope_name, description, is_deleted)
            VALUES ('advisor', '导师', '培养与学位', '培养方案制定、报告审阅、答辩指导', FALSE)
            ON CONFLICT (role_code) DO UPDATE
            SET role_name = EXCLUDED.role_name,
                scope_name = EXCLUDED.scope_name,
                description = EXCLUDED.description,
                is_deleted = FALSE,
                updated_at = CURRENT_TIMESTAMP
            RETURNING id
            """
        )
        role_id = cur.fetchone()[0]

    for advisor_name in sorted(ALLOWED_ADVISOR_SET):
        username = USERNAME_MAP[advisor_name]
        metadata = ADVISOR_METADATA[advisor_name]
        cur.execute(
            """
            INSERT INTO dtlms_users (
                username, full_name, email, department_name, phone_number, password_hash, is_active, is_deleted, last_login_at
            ) VALUES (%s, %s, %s, %s, NULL, %s, TRUE, FALSE, NULL)
            ON CONFLICT (username) DO UPDATE
            SET full_name = EXCLUDED.full_name,
                email = COALESCE(NULLIF(dtlms_users.email, ''), EXCLUDED.email),
                department_name = EXCLUDED.department_name,
                password_hash = COALESCE(NULLIF(dtlms_users.password_hash, ''), EXCLUDED.password_hash),
                is_active = TRUE,
                is_deleted = FALSE,
                updated_at = CURRENT_TIMESTAMP
            RETURNING id
            """,
            (username, advisor_name, f"{username}@dtlms.local", metadata["department_name"], DEFAULT_PASSWORD_HASH),
        )
        user_id = cur.fetchone()[0]
        stats["advisor_users_upserted"] += 1
        cur.execute(
            """
            INSERT INTO dtlms_user_roles (user_id, role_id, grant_source)
            VALUES (%s, %s, 'official_center_cleanup')
            ON CONFLICT (user_id, role_id) DO UPDATE
            SET grant_source = EXCLUDED.grant_source,
                updated_at = CURRENT_TIMESTAMP
            """,
            (user_id, role_id),
        )
        if table_exists(cur, "dtlms_user_profiles"):
            cur.execute(
                """
                INSERT INTO dtlms_user_profiles (
                    username, full_name, role_name, department_name, phone_number, email, theme_color
                ) VALUES (%s, %s, '导师', %s, NULL, %s, '#13795b')
                ON CONFLICT (username) DO UPDATE
                SET full_name = EXCLUDED.full_name,
                    role_name = EXCLUDED.role_name,
                    department_name = EXCLUDED.department_name,
                    email = COALESCE(dtlms_user_profiles.email, EXCLUDED.email),
                    theme_color = EXCLUDED.theme_color,
                    updated_at = CURRENT_TIMESTAMP
                """,
                (username, advisor_name, metadata["department_name"], f"{username}@dtlms.local"),
            )


def sync_runtime_advisor_users(cur, stats: dict[str, Any]) -> None:
    if not table_exists(cur, "dtlms_runtime_system_users"):
        return
    has_runtime_profiles = table_exists(cur, "dtlms_runtime_profiles")
    cur.execute(
        """
        SELECT
            u.id,
            u.username,
            u.full_name,
            COALESCE(up.department_name, u.department_name, '') AS department_name,
            COALESCE(up.phone_number, u.phone_number) AS phone_number,
            COALESCE(NULLIF(up.email, ''), NULLIF(u.email, ''), CONCAT(u.username, '@dtlms.local')) AS email,
            u.password_hash,
            u.is_active,
            u.last_login_at
        FROM dtlms_users u
        LEFT JOIN dtlms_user_profiles up ON up.username = u.username
        WHERE u.is_deleted = FALSE
          AND u.full_name = ANY(%s)
        ORDER BY u.id
        """,
        (sorted(ALLOWED_ADVISOR_SET),),
    )
    rows = cur.fetchall()
    for user_id, username, full_name, department_name, phone_number, email, password_hash, is_active, last_login_at in rows:
        payload = {
            "id": user_id,
            "username": username,
            "full_name": full_name,
            "role_code": "advisor",
            "department_name": department_name,
            "phone_number": phone_number,
            "account_status": "启用" if is_active else "停用",
            "last_login_at": last_login_at.strftime("%Y-%m-%d %H:%M:%S") if last_login_at else None,
            "password_hash": password_hash,
        }
        cur.execute(
            """
            INSERT INTO dtlms_runtime_system_users (id, payload, updated_at)
            VALUES (%s, %s::jsonb, CURRENT_TIMESTAMP)
            ON CONFLICT (id) DO UPDATE
            SET payload = EXCLUDED.payload,
                updated_at = CURRENT_TIMESTAMP
            """,
            (user_id, json.dumps(payload, ensure_ascii=False)),
        )
        stats["runtime_advisor_users_upserted"] += 1
        if has_runtime_profiles:
            profile_payload = {
                "username": username,
                "full_name": full_name,
                "role_name": "导师",
                "department_name": department_name,
                "phone_number": phone_number,
                "email": email,
                "theme_color": "#13795b",
            }
            cur.execute(
                """
                INSERT INTO dtlms_runtime_profiles (username, payload, updated_at)
                VALUES (%s, %s::jsonb, CURRENT_TIMESTAMP)
                ON CONFLICT (username) DO UPDATE
                SET payload = EXCLUDED.payload,
                    updated_at = CURRENT_TIMESTAMP
                """,
                (username, json.dumps(profile_payload, ensure_ascii=False)),
            )
            stats["runtime_advisor_profiles_upserted"] += 1


def ensure_teams(cur, stats: dict[str, Any]) -> None:
    max_no = fetch_scalar(
        cur,
        "SELECT COALESCE(MAX(CAST(SUBSTRING(team_code FROM 8) AS INTEGER)), 0) FROM dtlms_teams WHERE team_code ~ '^CENTER-[0-9]+$'",
    ) or 0
    next_no = int(max_no)
    advisor_name_to_id = {normalize_text(name): advisor_id for advisor_id, name in cur.execute("SELECT id, full_name FROM dtlms_advisors WHERE is_deleted = FALSE").fetchall()} if False else {}
    cur.execute("SELECT id, full_name FROM dtlms_advisors WHERE is_deleted = FALSE")
    advisor_name_to_id = {normalize_text(name): advisor_id for advisor_id, name in cur.fetchall()}

    for spec in TEAM_SPECS:
        lead_id = advisor_name_to_id[spec["lead"]]
        cur.execute(
            """
            UPDATE dtlms_teams
            SET department_name = %s,
                discipline_name = COALESCE(NULLIF(discipline_name, ''), '未分配学科'),
                lead_advisor_id = %s,
                research_directions = NULL,
                team_status = 'active',
                established_on = COALESCE(established_on, CURRENT_DATE),
                description = '按研究中心正式名单清理脚本维护。',
                is_deleted = FALSE,
                updated_at = CURRENT_TIMESTAMP
            WHERE team_name = %s
            """,
            (spec["team_name"], lead_id, spec["team_name"]),
        )
        if cur.rowcount:
            stats["teams_updated"] += cur.rowcount
            continue
        next_no += 1
        cur.execute(
            """
            INSERT INTO dtlms_teams (
                team_code, team_name, department_name, discipline_name, lead_advisor_id,
                research_directions, team_status, established_on, description, is_deleted
            ) VALUES (%s, %s, %s, '未分配学科', %s, NULL, 'active', CURRENT_DATE, '按研究中心正式名单清理脚本维护。', FALSE)
            """,
            (f"CENTER-{next_no:03d}", spec["team_name"], spec["team_name"], lead_id),
        )
        stats["teams_inserted"] += 1


def rebuild_team_advisors(cur, stats: dict[str, Any]) -> None:
    team_name_to_id, advisor_name_to_id = load_name_id_maps(cur)
    allowed_team_ids = [team_name_to_id[name] for name in TEAM_ORDER]
    cur.execute(
        "UPDATE dtlms_team_advisors SET is_deleted = TRUE, left_on = CURRENT_DATE, updated_at = CURRENT_TIMESTAMP WHERE team_id = ANY(%s)",
        (allowed_team_ids,),
    )
    stats["team_advisor_rows_soft_deleted"] += cur.rowcount

    for spec in TEAM_SPECS:
        team_id = team_name_to_id[spec["team_name"]]
        for advisor_name in spec["advisors"]:
            advisor_id = advisor_name_to_id[advisor_name]
            role = "lead" if advisor_name == spec["lead"] else "member"
            cur.execute(
                """
                INSERT INTO dtlms_team_advisors (team_id, advisor_id, advisor_role, joined_on, left_on, is_deleted)
                VALUES (%s, %s, %s, CURRENT_DATE, NULL, FALSE)
                ON CONFLICT (team_id, advisor_id) DO UPDATE
                SET advisor_role = EXCLUDED.advisor_role,
                    joined_on = COALESCE(dtlms_team_advisors.joined_on, EXCLUDED.joined_on),
                    left_on = NULL,
                    is_deleted = FALSE,
                    updated_at = CURRENT_TIMESTAMP
                """,
                (team_id, advisor_id, role),
            )
            stats["team_advisor_rows_upserted"] += 1


def sync_runtime_team_rows(cur, stats: dict[str, Any]) -> None:
    if not table_exists(cur, "dtlms_runtime_teams"):
        return
    cur.execute(
        """
        SELECT t.id, t.team_code, t.team_name, t.department_name, t.discipline_name, t.established_on, t.description, a.full_name
        FROM dtlms_teams t
        LEFT JOIN dtlms_advisors a ON a.id = t.lead_advisor_id
        WHERE t.is_deleted = FALSE AND t.team_name = ANY(%s)
        ORDER BY t.id
        """,
        (TEAM_ORDER,),
    )
    rows = cur.fetchall()
    for team_id, team_code, team_name, department_name, discipline_name, established_on, description, lead_name in rows:
        payload = {
            "id": team_id,
            "team_code": team_code,
            "team_name": team_name,
            "department_name": department_name or team_name,
            "discipline_name": normalize_text(discipline_name) or "未分配学科",
            "lead_advisor_name": normalize_text(lead_name),
            "advisor_names": TEAM_TO_ADVISORS[team_name],
            "research_directions": [],
            "status": "启用",
            "created_on": established_on.isoformat() if established_on else None,
            "established_on": established_on.isoformat() if established_on else None,
            "description": normalize_text(description) or "按研究中心正式名单清理脚本维护。",
        }
        cur.execute(
            """
            INSERT INTO dtlms_runtime_teams (id, payload, updated_at)
            VALUES (%s, %s::jsonb, CURRENT_TIMESTAMP)
            ON CONFLICT (id) DO UPDATE
            SET payload = EXCLUDED.payload,
                updated_at = CURRENT_TIMESTAMP
            """,
            (team_id, json.dumps(payload, ensure_ascii=False)),
        )
        stats["runtime_team_rows_upserted"] += 1


def build_student_assignments(cur) -> tuple[list[dict[str, Any]], dict[int, tuple[str, str]]]:
    has_team_name_column = column_exists(cur, "dtlms_students", "team_name")
    team_name_sql = "COALESCE(NULLIF(s.team_name, ''), t.team_name)" if has_team_name_column else "t.team_name"
    cur.execute(
        f"""
        SELECT
            s.id,
            s.student_no,
            s.full_name,
            s.team_id,
            s.primary_advisor_id,
            {team_name_sql} AS current_team_name,
            a.full_name AS current_advisor_name
        FROM dtlms_students s
        LEFT JOIN dtlms_teams t ON t.id = s.team_id
        LEFT JOIN dtlms_advisors a ON a.id = s.primary_advisor_id
        WHERE s.is_deleted = FALSE
        ORDER BY s.id
        """
    )
    assignments: list[dict[str, Any]] = []
    assignment_map: dict[int, tuple[str, str]] = {}
    for row in cur.fetchall():
        student_id, student_no, full_name, team_id, advisor_id, current_team_name, current_advisor_name = row
        current_team_name = normalize_text(current_team_name)
        current_advisor_name = normalize_text(current_advisor_name)
        valid_pair = current_team_name in ALLOWED_TEAM_SET and current_advisor_name in TEAM_TO_ADVISORS.get(current_team_name, [])
        if valid_pair:
            continue
        target_team, target_advisor = canonical_team_and_advisor(current_team_name, current_advisor_name, f"student:{student_id}:{student_no}:{full_name}")
        assignments.append(
            {
                "student_id": student_id,
                "student_no": student_no,
                "full_name": full_name,
                "current_team_name": current_team_name,
                "current_advisor_name": current_advisor_name,
                "target_team_name": target_team,
                "target_advisor_name": target_advisor,
            }
        )
        assignment_map[int(student_id)] = (target_team, target_advisor)
    return assignments, assignment_map


def apply_student_assignments(cur, stats: dict[str, Any]) -> dict[int, tuple[str, str]]:
    has_team_name_column = column_exists(cur, "dtlms_students", "team_name")
    assignments, assignment_map = build_student_assignments(cur)
    if not assignments:
        return assignment_map

    team_name_to_id, advisor_name_to_id = load_name_id_maps(cur)
    disallowed_team_ids = [team_id for name, team_id in team_name_to_id.items() if name not in ALLOWED_TEAM_SET]
    disallowed_advisor_ids = [advisor_id for name, advisor_id in advisor_name_to_id.items() if name not in ALLOWED_ADVISOR_SET]

    for item in assignments:
        student_id = item["student_id"]
        target_team_id = team_name_to_id[item["target_team_name"]]
        target_advisor_id = advisor_name_to_id[item["target_advisor_name"]]
        if has_team_name_column:
            cur.execute(
                "UPDATE dtlms_students SET team_id = %s, primary_advisor_id = %s, team_name = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s",
                (target_team_id, target_advisor_id, item["target_team_name"], student_id),
            )
        else:
            cur.execute(
                "UPDATE dtlms_students SET team_id = %s, primary_advisor_id = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s",
                (target_team_id, target_advisor_id, student_id),
            )
        stats["students_reassigned"] += 1

        if disallowed_team_ids:
            cur.execute(
                "UPDATE dtlms_student_team_history SET team_id = %s, updated_at = CURRENT_TIMESTAMP WHERE student_id = %s AND team_id = ANY(%s)",
                (target_team_id, student_id, disallowed_team_ids),
            )
            stats["student_team_history_reassigned"] += cur.rowcount
        if not fetch_scalar(cur, "SELECT 1 FROM dtlms_student_team_history WHERE student_id = %s AND team_id = %s AND end_date IS NULL", (student_id, target_team_id)):
            cur.execute(
                "INSERT INTO dtlms_student_team_history (student_id, team_id, start_date, end_date, change_reason) VALUES (%s, %s, CURRENT_DATE, NULL, %s)",
                (student_id, target_team_id, "official_center_cleanup"),
            )
            stats["student_team_history_inserted"] += 1

        if disallowed_advisor_ids:
            cur.execute(
                "UPDATE dtlms_student_advisor_history SET advisor_id = %s, updated_at = CURRENT_TIMESTAMP WHERE student_id = %s AND advisor_id = ANY(%s)",
                (target_advisor_id, student_id, disallowed_advisor_ids),
            )
            stats["student_advisor_history_reassigned"] += cur.rowcount
        if not fetch_scalar(cur, "SELECT 1 FROM dtlms_student_advisor_history WHERE student_id = %s AND advisor_id = %s AND end_date IS NULL", (student_id, target_advisor_id)):
            cur.execute(
                "INSERT INTO dtlms_student_advisor_history (student_id, advisor_id, relation_type, start_date, end_date, change_reason) VALUES (%s, %s, 'primary', CURRENT_DATE, NULL, %s)",
                (student_id, target_advisor_id, "official_center_cleanup"),
            )
            stats["student_advisor_history_inserted"] += 1

        cur.execute("UPDATE dtlms_training_plans SET advisor_id = %s, updated_at = CURRENT_TIMESTAMP WHERE student_id = %s AND is_deleted = FALSE", (target_advisor_id, student_id))
        stats["training_plans_reassigned"] += cur.rowcount
        cur.execute("UPDATE dtlms_outbound_studies SET advisor_id = %s, updated_at = CURRENT_TIMESTAMP WHERE student_id = %s AND is_deleted = FALSE", (target_advisor_id, student_id))
        stats["outbound_studies_reassigned"] += cur.rowcount
        cur.execute("UPDATE dtlms_theses SET advisor_id = %s, updated_at = CURRENT_TIMESTAMP WHERE student_id = %s AND is_deleted = FALSE", (target_advisor_id, student_id))
        stats["theses_reassigned"] += cur.rowcount
        cur.execute("UPDATE dtlms_scientific_reports SET reviewer_advisor_id = %s, updated_at = CURRENT_TIMESTAMP WHERE student_id = %s AND is_deleted = FALSE", (target_advisor_id, student_id))
        stats["scientific_reports_reassigned"] += cur.rowcount

    return assignment_map


def sync_runtime_students(cur, assignment_map: dict[int, tuple[str, str]], stats: dict[str, Any]) -> None:
    if not assignment_map or not table_exists(cur, "dtlms_runtime_students"):
        return
    with cur.connection.cursor(row_factory=dict_row) as runtime_cur:
        runtime_cur.execute("SELECT id, payload FROM dtlms_runtime_students WHERE id = ANY(%s)", (list(assignment_map.keys()),))
        rows = runtime_cur.fetchall()
        for row in rows:
            payload = row.get("payload") if isinstance(row, dict) else None
            if not isinstance(payload, dict):
                continue
            team_name, advisor_name = assignment_map[int(row["id"])]
            updated_payload = dict(payload)
            updated_payload["team_name"] = team_name
            updated_payload["advisor_name"] = advisor_name
            runtime_cur.execute(
                "UPDATE dtlms_runtime_students SET payload = %s::jsonb, updated_at = CURRENT_TIMESTAMP WHERE id = %s",
                (json.dumps(updated_payload, ensure_ascii=False), int(row["id"])),
            )
            stats["runtime_students_reassigned"] += 1


def update_portal_students(cur, stats: dict[str, Any]) -> dict[int, tuple[str, str]]:
    assignments: dict[int, tuple[str, str]] = {}
    if not table_exists(cur, "dtlms_portal_students"):
        return assignments
    with cur.connection.cursor(row_factory=dict_row) as portal_cur:
        portal_cur.execute("SELECT id, selected_team_name, selected_advisor_name, application_draft FROM dtlms_portal_students ORDER BY id")
        rows = portal_cur.fetchall()
        for row in rows:
            portal_student_id = int(row["id"])
            current_team = normalize_text(row.get("selected_team_name"))
            current_advisor = normalize_text(row.get("selected_advisor_name"))
            if current_team in ALLOWED_TEAM_SET and current_advisor in TEAM_TO_ADVISORS.get(current_team, []):
                continue
            target_team, target_advisor = canonical_team_and_advisor(current_team, current_advisor, f"portal-student:{portal_student_id}")
            updated_draft = row.get("application_draft") if isinstance(row.get("application_draft"), dict) else None
            if isinstance(updated_draft, dict):
                updated_draft = copy.deepcopy(updated_draft)
                updated_draft["selected_team_name"] = target_team
                updated_draft["selected_advisor_name"] = target_advisor
                if isinstance(updated_draft.get("preferences"), list):
                    for index, pref in enumerate(updated_draft["preferences"]):
                        if not isinstance(pref, dict):
                            continue
                        if index == 0:
                            pref["research_center_name"] = target_team
                            pref["advisor_name"] = target_advisor
                        else:
                            secondary_team = canonical_secondary_team(normalize_text(pref.get("research_center_name")), f"portal-student:{portal_student_id}:pref:{index}", exclude_team=target_team)
                            pref["research_center_name"] = secondary_team
                            if normalize_text(pref.get("advisor_name")):
                                _, secondary_advisor = canonical_team_and_advisor(secondary_team, normalize_text(pref.get("advisor_name")), f"portal-student:{portal_student_id}:pref:{index}")
                                pref["advisor_name"] = secondary_advisor
                if "first_choice" in updated_draft:
                    updated_draft["first_choice"] = target_team
                if "intended_advisor_name" in updated_draft:
                    updated_draft["intended_advisor_name"] = target_advisor
            portal_cur.execute(
                "UPDATE dtlms_portal_students SET selected_team_name = %s, selected_advisor_name = %s, application_draft = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s",
                (target_team, target_advisor, json.dumps(updated_draft, ensure_ascii=False) if updated_draft is not None else None, portal_student_id),
            )
            assignments[portal_student_id] = (target_team, target_advisor)
            stats["portal_students_reassigned"] += 1
    return assignments


def update_recruitment_applications(cur, stats: dict[str, Any]) -> dict[int, dict[str, Any]]:
    application_targets: dict[int, dict[str, Any]] = {}
    if not table_exists(cur, "dtlms_recruitment_applications"):
        return application_targets
    with cur.connection.cursor(row_factory=dict_row) as app_cur:
        app_cur.execute(
            "SELECT id, first_choice, second_choice, intended_advisor_name FROM dtlms_recruitment_applications WHERE is_deleted = FALSE ORDER BY id"
        )
        for row in app_cur.fetchall():
            app_id = int(row["id"])
            first_choice = normalize_text(row.get("first_choice"))
            second_choice = normalize_text(row.get("second_choice"))
            intended_advisor = normalize_text(row.get("intended_advisor_name"))
            target_first, target_advisor = canonical_team_and_advisor(first_choice, intended_advisor, f"recruitment:{app_id}:first")
            if second_choice:
                target_second = canonical_secondary_team(second_choice, f"recruitment:{app_id}:second", exclude_team=target_first)
            else:
                target_second = second_choice
            if first_choice == target_first and second_choice == target_second and intended_advisor == target_advisor:
                application_targets[app_id] = {
                    "first_choice": target_first,
                    "second_choice": target_second,
                    "intended_advisor_name": target_advisor,
                }
                continue
            app_cur.execute(
                "UPDATE dtlms_recruitment_applications SET first_choice = %s, second_choice = %s, intended_advisor_name = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s",
                (target_first, target_second or None, target_advisor, app_id),
            )
            stats["recruitment_applications_reassigned"] += 1
            application_targets[app_id] = {
                "first_choice": target_first,
                "second_choice": target_second,
                "intended_advisor_name": target_advisor,
            }
    return application_targets


def update_portal_preferences(cur, app_targets: dict[int, dict[str, Any]], stats: dict[str, Any]) -> None:
    if not app_targets or not table_exists(cur, "dtlms_portal_application_preferences"):
        return
    with cur.connection.cursor(row_factory=dict_row) as pref_cur:
        pref_cur.execute(
            "SELECT id, application_id, preference_order, research_center_name, advisor_name, is_optional FROM dtlms_portal_application_preferences ORDER BY application_id, preference_order, id"
        )
        for row in pref_cur.fetchall():
            application_id = int(row["application_id"])
            target = app_targets.get(application_id)
            if not target:
                continue
            pref_order = int(row["preference_order"])
            current_center = normalize_text(row.get("research_center_name"))
            current_advisor = normalize_text(row.get("advisor_name"))
            if pref_order == 1:
                target_center = target["first_choice"]
                target_advisor = target["intended_advisor_name"]
            else:
                target_center = target["second_choice"] or canonical_secondary_team(current_center, f"pref:{row['id']}", exclude_team=target["first_choice"])
                if normalize_text(row.get("advisor_name")):
                    _, target_advisor = canonical_team_and_advisor(target_center, current_advisor, f"pref:{row['id']}:advisor")
                else:
                    target_advisor = None if bool(row.get("is_optional")) else stable_pick(f"pref:{row['id']}:advisor", TEAM_TO_ADVISORS[target_center])
            if current_center == target_center and current_advisor == normalize_text(target_advisor):
                continue
            pref_cur.execute(
                "UPDATE dtlms_portal_application_preferences SET research_center_name = %s, advisor_name = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s",
                (target_center, target_advisor, int(row["id"])),
            )
            stats["portal_preferences_reassigned"] += 1


def sync_runtime_portal_students(cur, portal_assignments: dict[int, tuple[str, str]], stats: dict[str, Any]) -> None:
    if not portal_assignments or not table_exists(cur, "dtlms_runtime_portal_students"):
        return
    with cur.connection.cursor(row_factory=dict_row) as runtime_cur:
        runtime_cur.execute("SELECT id, payload FROM dtlms_runtime_portal_students WHERE id = ANY(%s)", (list(portal_assignments.keys()),))
        for row in runtime_cur.fetchall():
            payload = row.get("payload") if isinstance(row, dict) else None
            if not isinstance(payload, dict):
                continue
            target_team, target_advisor = portal_assignments[int(row["id"])]
            updated_payload = copy.deepcopy(payload)
            updated_payload["selected_team_name"] = target_team
            updated_payload["selected_advisor_name"] = target_advisor
            draft = updated_payload.get("application_draft")
            if isinstance(draft, dict):
                draft["selected_team_name"] = target_team
                draft["selected_advisor_name"] = target_advisor
            runtime_cur.execute(
                "UPDATE dtlms_runtime_portal_students SET payload = %s::jsonb, updated_at = CURRENT_TIMESTAMP WHERE id = %s",
                (json.dumps(updated_payload, ensure_ascii=False), int(row["id"])),
            )
            stats["runtime_portal_students_reassigned"] += 1


def reassign_projects(cur, stats: dict[str, Any]) -> None:
    if not table_exists(cur, "dtlms_research_projects"):
        return
    with cur.connection.cursor(row_factory=dict_row) as project_cur:
        project_cur.execute(
            """
            SELECT rp.id, rp.project_code, a.full_name AS advisor_name
            FROM dtlms_research_projects rp
            LEFT JOIN dtlms_advisors a ON a.id = rp.principal_advisor_id
            WHERE rp.is_deleted = FALSE
            ORDER BY rp.id
            """
        )
        project_cur.execute("SELECT id, full_name FROM dtlms_advisors WHERE is_deleted = FALSE")
        advisor_name_to_id = {normalize_text(name): advisor_id for advisor_id, name in project_cur.fetchall()}
        project_cur.execute(
            """
            SELECT rp.id, rp.project_code, a.full_name AS advisor_name
            FROM dtlms_research_projects rp
            LEFT JOIN dtlms_advisors a ON a.id = rp.principal_advisor_id
            WHERE rp.is_deleted = FALSE
            ORDER BY rp.id
            """
        )
        for row in project_cur.fetchall():
            current_name = normalize_text(row.get("advisor_name"))
            if current_name in ALLOWED_ADVISOR_SET:
                continue
            target_name = stable_pick(f"project:{row['id']}:{normalize_text(row.get('project_code'))}", sorted(ALLOWED_ADVISOR_SET))
            project_cur.execute(
                "UPDATE dtlms_research_projects SET principal_advisor_id = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s",
                (advisor_name_to_id[target_name], int(row["id"])),
            )
            stats["research_projects_reassigned"] += 1


def cleanup_disallowed_entities(cur, stats: dict[str, Any]) -> None:
    cur.execute("SELECT id FROM dtlms_teams WHERE is_deleted = FALSE AND team_name <> ALL(%s)", (TEAM_ORDER,))
    disallowed_team_ids = [row[0] for row in cur.fetchall()]
    cur.execute("SELECT id, full_name FROM dtlms_advisors WHERE is_deleted = FALSE")
    disallowed_advisors = [(advisor_id, normalize_text(name)) for advisor_id, name in cur.fetchall() if normalize_text(name) not in ALLOWED_ADVISOR_SET]
    disallowed_advisor_ids = [item[0] for item in disallowed_advisors]

    if disallowed_team_ids:
        cur.execute("UPDATE dtlms_team_advisors SET is_deleted = TRUE, left_on = CURRENT_DATE, updated_at = CURRENT_TIMESTAMP WHERE team_id = ANY(%s)", (disallowed_team_ids,))
        stats["disallowed_team_links_soft_deleted"] += cur.rowcount
        cur.execute("UPDATE dtlms_teams SET is_deleted = TRUE, updated_at = CURRENT_TIMESTAMP WHERE id = ANY(%s)", (disallowed_team_ids,))
        stats["disallowed_teams_soft_deleted"] += cur.rowcount
        if table_exists(cur, "dtlms_runtime_teams"):
            cur.execute("DELETE FROM dtlms_runtime_teams WHERE id = ANY(%s)", (disallowed_team_ids,))
            stats["runtime_disallowed_teams_deleted"] += cur.rowcount

    if disallowed_advisor_ids:
        cur.execute("UPDATE dtlms_team_advisors SET is_deleted = TRUE, left_on = CURRENT_DATE, updated_at = CURRENT_TIMESTAMP WHERE advisor_id = ANY(%s)", (disallowed_advisor_ids,))
        stats["disallowed_advisor_links_soft_deleted"] += cur.rowcount
        cur.execute("UPDATE dtlms_advisors SET is_deleted = TRUE, updated_at = CURRENT_TIMESTAMP WHERE id = ANY(%s)", (disallowed_advisor_ids,))
        stats["disallowed_advisors_soft_deleted"] += cur.rowcount
        if table_exists(cur, "dtlms_users"):
            disallowed_full_names = [name for _, name in disallowed_advisors]
            if disallowed_full_names:
                cur.execute(
                    "UPDATE dtlms_users SET is_active = FALSE, is_deleted = TRUE, updated_at = CURRENT_TIMESTAMP WHERE full_name = ANY(%s)",
                    (disallowed_full_names,),
                )
                stats["disallowed_advisor_users_disabled"] += cur.rowcount
                if table_exists(cur, "dtlms_runtime_system_users"):
                    cur.execute(
                        "DELETE FROM dtlms_runtime_system_users WHERE COALESCE(payload ->> 'full_name', '') = ANY(%s)",
                        (disallowed_full_names,),
                    )
                    stats["runtime_disallowed_advisor_users_deleted"] += cur.rowcount
                if table_exists(cur, "dtlms_runtime_profiles"):
                    cur.execute(
                        "DELETE FROM dtlms_runtime_profiles WHERE COALESCE(payload ->> 'full_name', '') = ANY(%s)",
                        (disallowed_full_names,),
                    )
                    stats["runtime_disallowed_advisor_profiles_deleted"] += cur.rowcount


def collect_baseline(cur) -> dict[str, int]:
    baseline = {
        "teams_total": 0,
        "teams_disallowed": 0,
        "advisors_total": 0,
        "advisors_disallowed": 0,
        "students_bad_team_or_advisor": 0,
    }
    baseline["teams_total"] = int(fetch_scalar(cur, "SELECT COUNT(*) FROM dtlms_teams WHERE is_deleted = FALSE") or 0)
    baseline["teams_disallowed"] = int(fetch_scalar(cur, "SELECT COUNT(*) FROM dtlms_teams WHERE is_deleted = FALSE AND team_name <> ALL(%s)", (TEAM_ORDER,)) or 0)
    baseline["advisors_total"] = int(fetch_scalar(cur, "SELECT COUNT(*) FROM dtlms_advisors WHERE is_deleted = FALSE") or 0)
    cur.execute("SELECT full_name FROM dtlms_advisors WHERE is_deleted = FALSE")
    baseline["advisors_disallowed"] = sum(1 for row in cur.fetchall() if normalize_text(row[0]) not in ALLOWED_ADVISOR_SET)
    _, assignment_map = build_student_assignments(cur)
    baseline["students_bad_team_or_advisor"] = len(assignment_map)
    return baseline


def build_summary(cur, stats: dict[str, Any], before: dict[str, int]) -> dict[str, Any]:
    after = collect_baseline(cur)
    return {
        "database": settings.postgres_db,
        "before": before,
        "after": after,
        "stats": stats,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Keep only official centers and advisors, and reassign linked data.")
    parser.add_argument("--dry-run", action="store_true", help="Read and simulate only; do not commit changes.")
    parser.add_argument("--summary", action="store_true", help="Print compact JSON summary.")
    parser.add_argument("--apply", action="store_true", help="Explicitly apply changes. If omitted, dry-run is implied.")
    args = parser.parse_args()

    dry_run = bool(args.dry_run or not args.apply)
    stats: dict[str, Any] = {
        "advisors_updated": 0,
        "advisors_inserted": 0,
        "advisor_users_upserted": 0,
        "runtime_advisor_users_upserted": 0,
        "runtime_advisor_profiles_upserted": 0,
        "teams_updated": 0,
        "teams_inserted": 0,
        "team_advisor_rows_soft_deleted": 0,
        "team_advisor_rows_upserted": 0,
        "students_reassigned": 0,
        "student_team_history_reassigned": 0,
        "student_team_history_inserted": 0,
        "student_advisor_history_reassigned": 0,
        "student_advisor_history_inserted": 0,
        "training_plans_reassigned": 0,
        "outbound_studies_reassigned": 0,
        "theses_reassigned": 0,
        "scientific_reports_reassigned": 0,
        "research_projects_reassigned": 0,
        "portal_students_reassigned": 0,
        "portal_preferences_reassigned": 0,
        "recruitment_applications_reassigned": 0,
        "runtime_students_reassigned": 0,
        "runtime_portal_students_reassigned": 0,
        "runtime_team_rows_upserted": 0,
        "disallowed_team_links_soft_deleted": 0,
        "disallowed_teams_soft_deleted": 0,
        "runtime_disallowed_teams_deleted": 0,
        "disallowed_advisor_links_soft_deleted": 0,
        "disallowed_advisors_soft_deleted": 0,
        "disallowed_advisor_users_disabled": 0,
        "runtime_disallowed_advisor_users_deleted": 0,
        "runtime_disallowed_advisor_profiles_deleted": 0,
    }

    with connect(autocommit=False) as conn:
        with conn.cursor() as cur:
            before = collect_baseline(cur)
            ensure_advisors(cur, stats, apply_changes=not dry_run)
            ensure_advisor_users(cur, stats)
            sync_runtime_advisor_users(cur, stats)
            ensure_teams(cur, stats)
            rebuild_team_advisors(cur, stats)
            sync_runtime_team_rows(cur, stats)
            student_assignment_map = apply_student_assignments(cur, stats)
            sync_runtime_students(cur, student_assignment_map, stats)
            portal_assignments = update_portal_students(cur, stats)
            app_targets = update_recruitment_applications(cur, stats)
            update_portal_preferences(cur, app_targets, stats)
            sync_runtime_portal_students(cur, portal_assignments, stats)
            reassign_projects(cur, stats)
            cleanup_disallowed_entities(cur, stats)

            if dry_run:
                summary = build_summary(cur, stats, before)
                conn.rollback()
            else:
                conn.commit()
                summary = build_summary(cur, stats, before)

    output = json.dumps(summary, ensure_ascii=False) if args.summary else json.dumps(summary, ensure_ascii=False, indent=2)
    print(output)


if __name__ == "__main__":
    main()