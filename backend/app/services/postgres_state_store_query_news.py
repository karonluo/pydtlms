"""News management PostgreSQL query mixin.

This module contains news article listing and CRUD query helpers.
"""

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

class PostgresStateStoreQueryNewsMixin:
    """Query mixin extracted by functional module."""

    def list_news_articles(self, keyword: str | None = None, news_type: str | None = None, status: str | None = None) -> list[dict[str, Any]]:
        """Execute query logic for `list_news_articles`."""
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
        """Execute query logic for `get_news_article_by_id`."""
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
        """Execute query logic for `create_news_article`."""
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
        """Execute query logic for `update_news_article`."""
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
        """Execute query logic for `delete_news_article`."""
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
        """Execute query logic for `publish_news_article`."""
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
        """Execute query logic for `offline_news_article`."""
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
        """Execute query logic for `batch_publish_news_articles`."""
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
        """Execute query logic for `batch_offline_news_articles`."""
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

    @staticmethod
    def _normalize_news_row(row: dict[str, Any]) -> dict[str, Any]:
        """Execute query logic for `_normalize_news_row`."""
        normalized: dict[str, Any] = {}
        for key, value in row.items():
            if isinstance(value, str):
                normalized[key] = value.strip()
            else:
                normalized[key] = value
        return normalized
