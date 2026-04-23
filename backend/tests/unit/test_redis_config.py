import pytest

from app.core import cache
from app.core.config import Settings


def test_settings_builds_single_redis_url() -> None:
    settings = Settings(
        redis_mode="single",
        redis_host="redis.internal",
        redis_port=6380,
        redis_db=3,
        redis_password="Pass@@word123!",
    )

    assert settings.redis_uses_sentinel is False
    assert settings.redis_url == "redis://:Pass%40%40word123%21@redis.internal:6380/3"
    assert settings.redis_celery_transport_options == {}


def test_settings_builds_sentinel_redis_url() -> None:
    settings = Settings(
        redis_mode="sentinel",
        redis_host_list="10.0.0.1:26379,10.0.0.2:26379",
        redis_sentinel_name="mymaster",
    )

    assert settings.redis_uses_sentinel is True
    assert settings.redis_sentinel_nodes == [("10.0.0.1", 26379), ("10.0.0.2", 26379)]
    assert settings.redis_url == "sentinel://10.0.0.1:26379;sentinel://10.0.0.2:26379"
    assert settings.redis_celery_transport_options == {"master_name": "mymaster"}


def test_get_cache_client_uses_single_mode_direct_connection(monkeypatch) -> None:
    captured: dict[str, object] = {}

    class FakeRedis:
        def __init__(self, **kwargs) -> None:
            captured.update(kwargs)

    monkeypatch.setattr(cache, "Redis", FakeRedis)
    monkeypatch.setattr(cache.settings, "redis_mode", "single")
    monkeypatch.setattr(cache.settings, "redis_host", "127.0.0.9")
    monkeypatch.setattr(cache.settings, "redis_port", 6381)
    monkeypatch.setattr(cache.settings, "redis_db", 5)
    monkeypatch.setattr(cache.settings, "redis_password", "secret")

    client = cache.get_cache_client()

    assert isinstance(client, FakeRedis)
    assert captured["host"] == "127.0.0.9"
    assert captured["port"] == 6381
    assert captured["db"] == 5
    assert captured["password"] == "secret"


def test_get_cache_client_uses_sentinel_master(monkeypatch) -> None:
    sentinel_calls: dict[str, object] = {}
    sentinel_client = object()

    class FakeSentinel:
        def master_for(self, name: str, **kwargs):
            sentinel_calls["name"] = name
            sentinel_calls.update(kwargs)
            return sentinel_client

    monkeypatch.setattr(cache, "get_sentinel", lambda: FakeSentinel())
    monkeypatch.setattr(cache.settings, "redis_mode", "sentinel")
    monkeypatch.setattr(cache.settings, "redis_sentinel_name", "cluster-master")
    monkeypatch.setattr(cache.settings, "redis_db", 2)
    monkeypatch.setattr(cache.settings, "redis_password", "sentinel-secret")

    client = cache.get_cache_client()

    assert client is sentinel_client
    assert sentinel_calls["name"] == "cluster-master"
    assert sentinel_calls["db"] == 2
    assert sentinel_calls["password"] == "sentinel-secret"


def test_get_sentinel_uses_dedicated_sentinel_password(monkeypatch) -> None:
    captured: dict[str, object] = {}

    class FakeSentinel:
        def __init__(self, nodes, **kwargs) -> None:
            captured["nodes"] = nodes
            captured.update(kwargs)

    cache.get_sentinel.cache_clear()
    monkeypatch.setattr(cache, "Sentinel", FakeSentinel)
    monkeypatch.setattr(cache.settings, "redis_mode", "sentinel")
    monkeypatch.setattr(cache.settings, "redis_host_list", "10.0.0.1:26379,10.0.0.2:26379")
    monkeypatch.setattr(cache.settings, "redis_db", 4)
    monkeypatch.setattr(cache.settings, "redis_password", "master-secret")
    monkeypatch.setattr(cache.settings, "redis_sentinel_password", "")

    sentinel = cache.get_sentinel()

    assert isinstance(sentinel, FakeSentinel)
    assert captured["nodes"] == [("10.0.0.1", 26379), ("10.0.0.2", 26379)]
    assert captured["sentinel_kwargs"]["password"] is None
    assert captured["password"] == "master-secret"
    assert captured["db"] == 4
    cache.get_sentinel.cache_clear()