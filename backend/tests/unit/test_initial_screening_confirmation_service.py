from __future__ import annotations

import json

from app.services.initial_screening_confirmation_service import list_initial_screening_confirmation_applications


class FakeCursor:
    def __init__(self, fetchone_results=None, fetchall_results=None) -> None:
        self.fetchone_results = list(fetchone_results or [])
        self.fetchall_results = list(fetchall_results or [])
        self.executed: list[tuple[str, object]] = []

    def execute(self, sql, params=None) -> None:
        self.executed.append((sql, params))

    def fetchone(self):
        if self.fetchone_results:
            return self.fetchone_results.pop(0)
        return None

    def fetchall(self):
        if self.fetchall_results:
            return self.fetchall_results.pop(0)
        return []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        return None


class FakeConnection:
    def __init__(self, cursor: FakeCursor) -> None:
        self.cursor_instance = cursor

    def cursor(self):
        return self.cursor_instance

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        return None


def test_list_initial_screening_confirmation_applications_builds_expected_filters(monkeypatch) -> None:
    cursor = FakeCursor(
        fetchone_results=[{"total": 1}],
        fetchall_results=[[{
            "application_id": 11,
            "student_id": 7,
            "plan_id": 5,
            "candidate_no": "SH20260011",
            "full_name": "张三",
            "first_choice": "刘亚",
            "first_choice_screening_score": 85,
            "second_choice": "王强",
            "second_choice_screening_score": None,
            "first_choice_screening_submitted_at": "2026-06-02 09:00:00",
            "second_choice_screening_submitted_at": None,
            "application_status": "initial_screening_confirmation",
            "intended_advisor_name": "刘亚",
        }]],
    )
    connection = FakeConnection(cursor)

    import app.services.initial_screening_confirmation_service as service_module

    monkeypatch.setattr(service_module.query_store, "_connect", lambda database_name: connection)
    monkeypatch.setattr(service_module.query_store, "_execute_dynamic", lambda cur, sql, params: cur.execute(sql, params))
    monkeypatch.setattr(service_module.query_store, "_normalize_recruitment_application_row", lambda row: row)

    response = list_initial_screening_confirmation_applications(
        plan_id=5,
        keyword="SH2026",
        advisor_names=["刘亚"],
        page=2,
        page_size=20,
    )

    assert response.total == 1
    assert response.page == 2
    assert response.page_size == 20
    assert response.items[0].candidate_no == "SH20260011"

    count_sql, count_params = cursor.executed[0]
    query_sql, query_params = cursor.executed[1]
    assert "app.application_status = 'initial_screening_confirmation'" in count_sql
    assert "stu.full_name ILIKE %s OR app.candidate_no ILIKE %s" in count_sql
    assert "TRIM(app.first_choice) = %s OR TRIM(app.second_choice) = %s" in count_sql
    assert count_params == [5, "%SH2026%", "%SH2026%", "刘亚", "刘亚"]
    assert query_params[-2:] == [20, 20]
    assert query_params[:-2] == count_params
