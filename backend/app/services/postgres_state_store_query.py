"""Aggregate PostgreSQL query mixin entrypoint.

This module composes the feature-specific query mixins so existing imports and
callers can continue using `PostgresStateStoreQueryMixin` without code changes.
"""

from __future__ import annotations

from app.services.postgres_state_store_query_base import PostgresStateStoreQueryBaseMixin
from app.services.postgres_state_store_query_dashboard import PostgresStateStoreQueryDashboardMixin
from app.services.postgres_state_store_query_news import PostgresStateStoreQueryNewsMixin
from app.services.postgres_state_store_query_recruitment import PostgresStateStoreQueryRecruitmentMixin
from app.services.postgres_state_store_query_students import PostgresStateStoreQueryStudentsMixin
from app.services.postgres_state_store_query_system import PostgresStateStoreQuerySystemMixin
from app.services.postgres_state_store_query_training_degree import PostgresStateStoreQueryTrainingDegreeMixin
from app.services.postgres_state_store_query_workflow import PostgresStateStoreQueryWorkflowMixin


class PostgresStateStoreQueryMixin(
    PostgresStateStoreQueryNewsMixin,
    PostgresStateStoreQueryDashboardMixin,
    PostgresStateStoreQueryTrainingDegreeMixin,
    PostgresStateStoreQueryWorkflowMixin,
    PostgresStateStoreQueryStudentsMixin,
    PostgresStateStoreQueryRecruitmentMixin,
    PostgresStateStoreQuerySystemMixin,
    PostgresStateStoreQueryBaseMixin,
):
    """Aggregate query mixin composed from feature-specific query modules."""

    pass
