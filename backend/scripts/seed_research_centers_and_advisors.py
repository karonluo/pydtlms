from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path


BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


from app.core.security import get_password_hash
from app.services.postgres_state_store import PostgresStateStore


DEFAULT_ADVISOR_PASSWORD = "ChangeMe@123"
DEFAULT_THEME_COLOR = "#13795b"


RAW_CENTER_SEEDS: tuple[dict[str, object], ...] = (
    {
        "center_name": "前沿探索中心",
        "director_name": "乔宇",
        "advisor_names": ("周伯文", "成宇", "石博天", "薛天帆", "蔡品隆", "邹娜", "刘翼豪", "何军军", "陈昕苑", "胡杨", "张超"),
    },
    {
        "center_name": "AI For Science中心",
        "director_name": "白磊",
        "advisor_names": ("周伯文", "欧阳万里", "张铂", "李玉强", "董楠卿", "宋纯锋", "胡舒悦", "王潚崧", "郝红霞"),
    },
    {
        "center_name": "大模型中心",
        "director_name": "陈恺",
        "advisor_names": ("周伯文", "林达华", "王利民", "张文蔚", "郭琦鹏", "王毅", "李亦宁", "张超", "张奇"),
    },
    {
        "center_name": "物理智能中心",
        "director_name": "张伟楠",
        "advisor_names": ("周伯文", "沈春华", "翟少鹏", "赵斌", "吕照阳", "穆尧", "沈渊"),
    },
    {
        "center_name": "安全可信AI中心",
        "director_name": "胡侠",
        "advisor_names": ("周伯文", "陆超超", "邵婧", "王迎春", "杨超", "滕妍", "瞿晶晶"),
    },
    {
        "center_name": "评测中心",
        "director_name": "翟广涛",
        "advisor_names": ("周伯文", "胡侠"),
    },
    {
        "center_name": "Data-CentricAI",
        "director_name": "何聪辉",
        "advisor_names": ("周伯文", "林达华", "王斌", "吴郦军", "吴江", "邱剑涛"),
    },
    {
        "center_name": "系统平台中心",
        "director_name": "林达华",
        "advisor_names": ("周伯文", "李恒杰"),
    },
)


USERNAME_BY_NAME: dict[str, str] = {
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


@dataclass(frozen=True)
class CenterSeed:
    center_name: str
    director_name: str
    advisor_names: tuple[str, ...]


@dataclass(frozen=True)
class AdvisorSeed:
    full_name: str
    username: str
    center_names: tuple[str, ...]
    lead_center_names: tuple[str, ...]

    @property
    def department_name(self) -> str:
        if self.lead_center_names:
            return self.lead_center_names[0]
        if len(self.center_names) == 1:
            return self.center_names[0]
        return "多中心联合"

    @property
    def research_direction(self) -> str:
        return "、".join(self.center_names)


def _dedupe_names(*groups: tuple[str, ...] | list[str] | set[str] | str) -> tuple[str, ...]:
    ordered: list[str] = []
    for group in groups:
        values = (group,) if isinstance(group, str) else group
        for value in values:
            item = str(value).strip()
            if item and item not in ordered:
                ordered.append(item)
    return tuple(ordered)


def build_center_seeds() -> list[CenterSeed]:
    seeds: list[CenterSeed] = []
    for item in RAW_CENTER_SEEDS:
        director_name = str(item["director_name"]).strip()
        advisor_names = _dedupe_names(director_name, tuple(item["advisor_names"]))
        seeds.append(
            CenterSeed(
                center_name=str(item["center_name"]).strip(),
                director_name=director_name,
                advisor_names=advisor_names,
            )
        )
    return seeds


def build_advisor_seeds(center_seeds: list[CenterSeed] | None = None) -> list[AdvisorSeed]:
    centers = center_seeds or build_center_seeds()
    assignments: dict[str, dict[str, list[str]]] = {}
    for center in centers:
        for advisor_name in center.advisor_names:
            current = assignments.setdefault(advisor_name, {"centers": [], "lead_centers": []})
            if center.center_name not in current["centers"]:
                current["centers"].append(center.center_name)
            if advisor_name == center.director_name and center.center_name not in current["lead_centers"]:
                current["lead_centers"].append(center.center_name)

    missing_usernames = sorted(name for name in assignments if name not in USERNAME_BY_NAME)
    if missing_usernames:
        raise KeyError(f"Missing usernames for advisors: {', '.join(missing_usernames)}")

    return [
        AdvisorSeed(
            full_name=name,
            username=USERNAME_BY_NAME[name],
            center_names=tuple(values["centers"]),
            lead_center_names=tuple(values["lead_centers"]),
        )
        for name, values in sorted(assignments.items(), key=lambda item: item[1]["centers"][0] + item[0])
    ]


def _next_available_id(cur, *table_names: str) -> int:
    values: list[int] = []
    for table_name in table_names:
        cur.execute(f"SELECT COALESCE(MAX(id), 0) FROM {table_name}")
        row = cur.fetchone()
        values.append(int(row[0] if row else 0))
    return max(values, default=0)


def _existing_user_rows(cur) -> list[dict[str, object]]:
    cur.execute(
        """
        SELECT
            u.id,
            u.username,
            u.full_name,
            u.department_name,
            u.phone_number,
            u.password_hash,
            u.is_active,
            u.last_login_at,
            COALESCE(r.role_code, '') AS role_code,
            COALESCE(up.email, u.email) AS email,
            COALESCE(up.theme_color, '#13795b') AS theme_color
        FROM dtlms_users u
        LEFT JOIN dtlms_user_roles ur ON ur.user_id = u.id
        LEFT JOIN dtlms_roles r ON r.id = ur.role_id AND r.is_deleted = FALSE
        LEFT JOIN dtlms_user_profiles up ON up.username = u.username
        WHERE u.is_deleted = FALSE
        """
    )
    columns = ("id", "username", "full_name", "department_name", "phone_number", "password_hash", "is_active", "last_login_at", "role_code", "email", "theme_color")
    return [dict(zip(columns, row, strict=True)) for row in cur.fetchall()]


def _upsert_advisors(store: PostgresStateStore, advisor_seeds: list[AdvisorSeed]) -> dict[str, int]:
    store.ensure_schema()
    with store._connect("db_dtlms") as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, advisor_no, full_name FROM dtlms_advisors WHERE full_name = ANY(%s) ORDER BY id",
                ([item.full_name for item in advisor_seeds],),
            )
            existing_rows = cur.fetchall()
            advisor_by_name = {str(row[2]): {"id": int(row[0]), "advisor_no": str(row[1])} for row in existing_rows}
            next_advisor_id = _next_available_id(cur, "dtlms_advisors")
            advisor_ids: dict[str, int] = {}

            for item in advisor_seeds:
                existing = advisor_by_name.get(item.full_name)
                if existing is None:
                    next_advisor_id += 1
                    advisor_id = next_advisor_id
                    advisor_no = f"ADV{advisor_id:03d}"
                    cur.execute(
                        """
                        INSERT INTO dtlms_advisors (
                            id, advisor_no, full_name, title, organization_name, research_direction, annual_quota, is_deleted
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, FALSE)
                        """,
                        (
                            advisor_id,
                            advisor_no,
                            item.full_name,
                            "导师",
                            item.department_name,
                            item.research_direction,
                            0,
                        ),
                    )
                else:
                    advisor_id = int(existing["id"])
                    cur.execute(
                        """
                        UPDATE dtlms_advisors
                        SET advisor_no = %s,
                            full_name = %s,
                            title = %s,
                            organization_name = %s,
                            research_direction = %s,
                            annual_quota = %s,
                            is_deleted = FALSE,
                            updated_at = CURRENT_TIMESTAMP
                        WHERE id = %s
                        """,
                        (
                            str(existing["advisor_no"]),
                            item.full_name,
                            "导师",
                            item.department_name,
                            item.research_direction,
                            0,
                            advisor_id,
                        ),
                    )
                advisor_ids[item.full_name] = advisor_id
        conn.commit()
    return advisor_ids


def _sync_system_users(store: PostgresStateStore, advisor_seeds: list[AdvisorSeed]) -> dict[str, int]:
    store.ensure_schema()
    with store._connect("db_dtlms") as conn:
        with conn.cursor() as cur:
            user_rows = _existing_user_rows(cur)
            next_user_id = _next_available_id(cur, "dtlms_users")

    users_by_username = {str(item["username"]): item for item in user_rows}
    users_by_name = {str(item["full_name"]): item for item in user_rows}
    user_ids: dict[str, int] = {}

    for item in advisor_seeds:
        existing = users_by_username.get(item.username)
        renamed_from: str | None = None
        if existing is None:
            candidate = users_by_name.get(item.full_name)
            if candidate and str(candidate.get("role_code") or "") in {"", "advisor"}:
                existing = candidate
                renamed_from = str(candidate["username"])
        if existing is None:
            next_user_id += 1
            user_id = next_user_id
            password_hash = get_password_hash(DEFAULT_ADVISOR_PASSWORD)
            phone_number = None
            last_login_at = None
            email = f"{item.username}@dtlms.local"
            theme_color = DEFAULT_THEME_COLOR
        else:
            user_id = int(existing["id"])
            password_hash = str(existing["password_hash"] or get_password_hash(DEFAULT_ADVISOR_PASSWORD))
            phone_number = str(existing["phone_number"]) if existing.get("phone_number") else None
            last_login_at = existing.get("last_login_at")
            email = str(existing["email"]) if existing.get("email") else f"{item.username}@dtlms.local"
            theme_color = str(existing["theme_color"] or DEFAULT_THEME_COLOR)

        user_payload = {
            "id": user_id,
            "username": item.username,
            "full_name": item.full_name,
            "role_code": "advisor",
            "department_name": item.department_name,
            "phone_number": phone_number,
            "account_status": "启用",
            "last_login_at": last_login_at,
            "password_hash": password_hash,
        }
        profile_payload = {
            "username": item.username,
            "full_name": item.full_name,
            "role_name": "导师",
            "department_name": item.department_name,
            "phone_number": phone_number,
            "email": email,
            "theme_color": theme_color,
        }
        store.sync_system_user(user_payload, profile_payload, counters={"system_users": max(next_user_id, user_id)})
        if renamed_from and renamed_from != item.username:
            store.delete_user_profile(renamed_from)
        user_ids[item.full_name] = user_id

    store.update_runtime_counter("system_users", next_user_id)
    return user_ids


def _sync_centers(store: PostgresStateStore, center_seeds: list[CenterSeed]) -> dict[str, int]:
    store.ensure_schema()
    today = date.today().isoformat()
    with store._connect("db_dtlms") as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, team_name, team_code, established_on FROM dtlms_teams WHERE team_name = ANY(%s) ORDER BY id",
                ([item.center_name for item in center_seeds],),
            )
            existing_rows = cur.fetchall()
            next_team_id = _next_available_id(cur, "dtlms_teams")

    teams_by_name = {
        str(row[1]): {
            "id": int(row[0]),
            "team_code": str(row[2]),
            "established_on": row[3].isoformat() if row[3] else today,
        }
        for row in existing_rows
    }
    team_ids: dict[str, int] = {}

    for item in center_seeds:
        existing = teams_by_name.get(item.center_name)
        if existing is None:
            next_team_id += 1
            team_id = next_team_id
            team_code = f"CENTER-{team_id:03d}"
            established_on = today
        else:
            team_id = int(existing["id"])
            team_code = str(existing["team_code"] or f"CENTER-{team_id:03d}")
            established_on = str(existing["established_on"] or today)

        team_payload = {
            "id": team_id,
            "team_code": team_code,
            "team_name": item.center_name,
            "department_name": item.center_name,
            "discipline_name": "未分配学科",
            "lead_advisor_name": item.director_name,
            "advisor_names": list(item.advisor_names),
            "research_directions": [],
            "status": "启用",
            "created_on": established_on,
            "established_on": established_on,
            "description": "按研究中心主数据维护需求批量导入。",
        }
        store.sync_updated_center(team_payload, affected_students=[], operation_log=None, counters={"teams": max(next_team_id, team_id)})
        team_ids[item.center_name] = team_id

    store.update_runtime_counter("teams", next_team_id)
    return team_ids


def seed_research_centers_and_advisors(*, summary_only: bool = False) -> dict[str, object]:
    center_seeds = build_center_seeds()
    advisor_seeds = build_advisor_seeds(center_seeds)
    store = PostgresStateStore()

    advisor_ids = _upsert_advisors(store, advisor_seeds)
    user_ids = _sync_system_users(store, advisor_seeds)
    team_ids = _sync_centers(store, center_seeds)

    summary = {
        "advisor_count": len(advisor_ids),
        "system_user_count": len(user_ids),
        "center_count": len(team_ids),
        "centers": [item.center_name for item in center_seeds],
        "sample_logins": {item.full_name: item.username for item in advisor_seeds[:10]},
    }
    if not summary_only:
        summary["all_logins"] = {item.full_name: item.username for item in advisor_seeds}
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed research centers, advisors, and advisor accounts into PostgreSQL.")
    parser.add_argument("--summary", action="store_true", help="Print summary only.")
    args = parser.parse_args()
    print(json.dumps(seed_research_centers_and_advisors(summary_only=args.summary), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
