from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


from app.services.management_service import store
from app.services.postgres_state_store import PostgresStateStore


def main() -> None:
    parser = argparse.ArgumentParser(description="Initialize PostgreSQL schema and demo data for DTLMS.")
    parser.add_argument("--summary", action="store_true", help="Print inserted dataset counts only.")
    args = parser.parse_args()

    pg_store = PostgresStateStore()
    pg_store.save_state(store.state)

    summary = {
        "database": "db_dtlms",
        "runtime_tables": len(pg_store.DATASET_TABLES) + 1,
        "students": len(store.state.get("students", [])),
        "recruitment_plans": len(store.state.get("recruitment_plans", [])),
        "recruitment_applications": len(store.state.get("recruitment_applications", [])),
        "training_plans": len(store.state.get("training_plans", [])),
        "scientific_reports": len(store.state.get("scientific_reports", [])),
        "outbound_studies": len(store.state.get("outbound_studies", [])),
        "theses": len(store.state.get("theses", [])),
        "workflow_tasks": len(store.state.get("workflow_tasks", [])),
        "system_users": len(store.state.get("system_users", [])),
    }
    if args.summary:
        print(json.dumps(summary, ensure_ascii=False))
        return

    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()