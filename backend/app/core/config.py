from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from urllib.parse import quote

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


BACKEND_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    app_name: str = "博士生生命周期管理系统"
    environment: str = "development"
    api_v1_prefix: str = "/api/v1"
    docs_url: str = "/docs"
    openapi_url: str = "/openapi.json"

    smtp_enabled: bool = False
    smtp_host: str = ""
    smtp_port: int = 465
    smtp_username: str = ""
    smtp_password: str = ""
    smtp_from_email: str = ""
    smtp_from_name: str = ""
    smtp_use_tls: bool = False
    smtp_use_ssl: bool = True
    smtp_timeout_seconds: int = 120

    postgres_host: str = "47.117.107.23"
    postgres_port: int = 15431
    postgres_user: str = "postgres"
    postgres_password: str = "Pass@@word123!"
    postgres_db: str = "db_dtlms"
    postgres_schema: str = "public"
    sqlalchemy_echo: bool = False

    jwt_secret_key: str = "replace-with-a-strong-secret"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_minutes: int = 60 * 24 * 7

    redis_mode: str = "sentinel"
    redis_host: str = "127.0.0.1"
    redis_port: int = 6379
    redis_db: int = 0
    redis_host_list: str = "47.117.107.23:41104,47.117.107.23:41105,47.117.107.23:41106"
    redis_password: str = "Pass@@word123!"
    redis_sentinel_password: str = ""
    redis_sentinel_name: str = "mymaster"
    redis_key_prefix: str = "CTDTLMS_"

    allowed_origins: str = "http://localhost:5173,http://127.0.0.1:5173"
    default_admin_username: str = "admin"
    default_admin_password: str = "Admin@123456"
    frontend_dev_proxy_enabled: bool = False
    frontend_dev_proxy_target: str = "http://127.0.0.1:5173"
    frontend_dev_proxy_timeout_seconds: float = 15.0
    portal_admissions_info_url: str = "https://www.shlab.org.cn"

    model_config = SettingsConfigDict(
        env_file=(BACKEND_DIR / ".env.local", BACKEND_DIR / ".env"),
        extra="ignore",
        case_sensitive=False,
    )

    @computed_field
    @property
    def sqlalchemy_database_uri(self) -> str:
        return (
            f"postgresql+psycopg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def allowed_origins_list(self) -> list[str]:
        return [item.strip() for item in self.allowed_origins.split(",") if item.strip()]

    @property
    def redis_mode_value(self) -> str:
        mode = self.redis_mode.strip().lower()
        if mode not in {"single", "sentinel"}:
            raise ValueError("REDIS_MODE 仅支持 single 或 sentinel")
        return mode

    @property
    def redis_uses_sentinel(self) -> bool:
        return self.redis_mode_value == "sentinel"

    @property
    def redis_password_encoded(self) -> str:
        return quote(self.redis_password, safe="") if self.redis_password else ""

    @property
    def redis_sentinel_nodes(self) -> list[tuple[str, int]]:
        if not self.redis_uses_sentinel:
            return []
        nodes: list[tuple[str, int]] = []
        host_items = [item.strip() for item in self.redis_host_list.split(",") if item.strip()]
        if not host_items:
            raise ValueError("REDIS_MODE=sentinel 时必须配置 REDIS_HOST_LIST")
        for item in host_items:
            host, port = item.split(":", 1)
            nodes.append((host.strip(), int(port.strip())))
        return nodes

    @property
    def redis_url(self) -> str:
        if self.redis_uses_sentinel:
            if not self.redis_sentinel_name.strip():
                raise ValueError("REDIS_MODE=sentinel 时必须配置 REDIS_SENTINEL_NAME")
            return ";".join(f"sentinel://{host}:{port}" for host, port in self.redis_sentinel_nodes)

        auth = f":{self.redis_password_encoded}@" if self.redis_password else ""
        return f"redis://{auth}{self.redis_host}:{self.redis_port}/{self.redis_db}"

    @property
    def redis_celery_transport_options(self) -> dict[str, str]:
        if not self.redis_uses_sentinel:
            return {}
        return {"master_name": self.redis_sentinel_name}


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
