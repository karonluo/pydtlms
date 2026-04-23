from __future__ import annotations

from functools import lru_cache

from redis import Redis
from redis.sentinel import Sentinel

from app.core.config import settings


@lru_cache
def get_sentinel() -> Sentinel:
    if not settings.redis_uses_sentinel:
        raise RuntimeError("当前 Redis 配置不是哨兵模式")
    return Sentinel(
        settings.redis_sentinel_nodes,
        sentinel_kwargs={"password": settings.redis_sentinel_password or None, "socket_timeout": 1},
        password=settings.redis_password or None,
        db=settings.redis_db,
        decode_responses=True,
        socket_connect_timeout=1,
        socket_timeout=1,
        retry_on_timeout=False,
    )


def _build_redis_client(host: str, port: int) -> Redis:
    return Redis(
        host=host,
        port=port,
        db=settings.redis_db,
        password=settings.redis_password or None,
        decode_responses=True,
        socket_connect_timeout=1,
        socket_timeout=1,
        retry_on_timeout=False,
    )


def get_cache_client() -> Redis:
    if not settings.redis_uses_sentinel:
        return _build_redis_client(settings.redis_host, settings.redis_port)

    sentinel = get_sentinel()
    return sentinel.master_for(
        settings.redis_sentinel_name,
        db=settings.redis_db,
        password=settings.redis_password or None,
        decode_responses=True,
        socket_connect_timeout=1,
        socket_timeout=1,
        retry_on_timeout=False,
    )


def build_cache_key(*segments: str) -> str:
    return settings.redis_key_prefix + ":".join(segments)
