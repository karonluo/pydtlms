from __future__ import annotations

from app.services.postgres_state_store_core import PostgresStateStoreCoreMixin
from app.services.postgres_state_store_query import PostgresStateStoreQueryMixin
from app.services.postgres_state_store_seed import PostgresStateStoreSeedMixin
from app.services.postgres_state_store_sync import PostgresStateStoreSyncMixin


class PostgresStateStore(
    PostgresStateStoreSeedMixin,
    PostgresStateStoreQueryMixin,
    PostgresStateStoreSyncMixin,
    PostgresStateStoreCoreMixin,
):
    pass
