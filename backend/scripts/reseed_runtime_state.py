from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


from app.core.security import get_password_hash
from app.services.postgres_state_store import PostgresStateStore
from app.services.runtime_seed_data import build_runtime_seed_state


DEFAULT_PASSWORD_BY_USERNAME = {
    "admin": "Admin@123456",
    "liu.ya": "LiuYa@2026",
    "yuan.ye": "YuanYe@2026",
    "xu.sutian": "XuSutian@2026",
    "zhou.qing": "ZhouQing@2026",
    "he.lin": "HeLin@2026",
    "cao.bo": "CaoBo@2026",
    "yang.qin": "YangQin@2026",
    "sun.wei": "SunWei@2026",
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Rebuild PostgreSQL runtime state with realistic seed data.")
    parser.add_argument("--summary", action="store_true", help="Print summary only.")
    args = parser.parse_args()

    state = build_runtime_seed_state()
    for user in state.get("system_users", []):
        password = DEFAULT_PASSWORD_BY_USERNAME.get(user["username"], "ChangeMe@123")
        user["password_hash"] = get_password_hash(password)

    postgres_store = PostgresStateStore()
    postgres_store.save_state(state)

    summary = {
        "students": len(state.get("students", [])),
        "teams": len(state.get("teams", [])),
        "recruitment_plans": len(state.get("recruitment_plans", [])),
        "recruitment_applications": len(state.get("recruitment_applications", [])),
        "training_plans": len(state.get("training_plans", [])),
        "scientific_reports": len(state.get("scientific_reports", [])),
        "outbound_studies": len(state.get("outbound_studies", [])),
        "theses": len(state.get("theses", [])),
        "system_users": len(state.get("system_users", [])),
    }
    if args.summary:
        print(json.dumps(summary, ensure_ascii=False))
        return

    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()