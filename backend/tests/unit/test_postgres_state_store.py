from pathlib import Path

from app.services.postgres_state_store import PostgresStateStore


class FakeCursor:
    def __init__(self, fetchone_results=None) -> None:
        self.fetchone_results = list(fetchone_results or [])
        self.executed: list[tuple[str, object]] = []

    def execute(self, sql, params=None) -> None:
        self.executed.append((sql, params))

    def fetchone(self):
        if self.fetchone_results:
            return self.fetchone_results.pop(0)
        return None

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


def test_build_dsn_includes_connect_timeout() -> None:
    store = PostgresStateStore()

    dsn = store._build_dsn("db_dtlms", "postgres")

    assert "dbname=db_dtlms" in dsn
    assert "user=postgres" in dsn
    assert f"connect_timeout={store.CONNECT_TIMEOUT_SECONDS}" in dsn


def test_schema_initialized_returns_true_when_runtime_table_exists() -> None:
    store = PostgresStateStore()
    cursor = FakeCursor(fetchone_results=[("public.dtlms_runtime_counters",)])

    assert store._schema_initialized(cursor) is True


def test_ensure_schema_skips_sql_execution_when_schema_exists(monkeypatch, tmp_path: Path) -> None:
    store = PostgresStateStore()
    store._sql_dir = tmp_path
    cursor = FakeCursor()
    connection = FakeConnection(cursor)

    monkeypatch.setattr(store, "ensure_database", lambda: None)
    monkeypatch.setattr(store, "_connect", lambda database_name, autocommit=False: connection)
    monkeypatch.setattr(store, "_schema_initialized", lambda cur: True)
    monkeypatch.setattr(store, "MIGRATION_SQL_FILES", ())

    store.ensure_schema()

    assert store._schema_ready is True
    assert cursor.executed == []


def test_ensure_schema_executes_sql_files_when_schema_missing(monkeypatch, tmp_path: Path) -> None:
    store = PostgresStateStore()
    store._sql_dir = tmp_path
    cursor = FakeCursor()
    connection = FakeConnection(cursor)
    expected_sql: list[str] = []

    for file_name in store.SQL_FILES[1:]:
        sql_text = f"-- {file_name}\nSELECT '{file_name}';"
        expected_sql.append(sql_text)
        (tmp_path / file_name).write_text(sql_text, encoding="utf-8")

    monkeypatch.setattr(store, "ensure_database", lambda: None)
    monkeypatch.setattr(store, "_connect", lambda database_name, autocommit=False: connection)
    monkeypatch.setattr(store, "_schema_initialized", lambda cur: False)

    store.ensure_schema()

    assert store._schema_ready is True
    assert [sql for sql, _ in cursor.executed] == expected_sql