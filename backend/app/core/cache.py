from __future__ import annotations

from functools import lru_cache

from redis import Redis
from redis.sentinel import Sentinel

from app.core.config import settings


@lru_cache
def get_sentinel() -> Sentinel:
    return Sentinel(
        settings.redis_sentinel_nodes,
        password=settings.redis_password or None,
        decode_responses=True,
        socket_timeout=1,
    )


def get_cache_client() -> Redis:
    sentinel = get_sentinel()
    try:
        host, port = sentinel.discover_master(settings.redis_sentinel_name)
        return Redis(
            host=host,
            port=port,
            password=settings.redis_password or None,
            decode_responses=True,
            socket_connect_timeout=1,
            socket_timeout=1,
            retry_on_timeout=False,
        )
    except Exception:
        host, port = settings.redis_sentinel_nodes[0]
        return Redis(
            host=host,
            port=port,
            password=settings.redis_password or None,
            decode_responses=True,
            socket_connect_timeout=1,
            socket_timeout=1,
            retry_on_timeout=False,
        )


def build_cache_key(*segments: str) -> str:
    return settings.redis_key_prefix + ":".join(segments)
