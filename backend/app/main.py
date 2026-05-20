import json
from time import perf_counter

import httpx
from fastapi import APIRouter, FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import auth, dashboard, degree, portal, recruitment, students, system, training, workflow
from app.core.config import settings
from app.core.exceptions import DatabaseUnavailableError
from app.core.logging import configure_logging
from app.services.management_service import repair_startup_postgres_state, warm_up_runtime_management_store


logger = configure_logging()

_HOP_BY_HOP_HEADERS = {
    "connection",
    "content-length",
    "host",
    "keep-alive",
    "proxy-authenticate",
    "proxy-authorization",
    "te",
    "trailer",
    "transfer-encoding",
    "upgrade",
}

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    docs_url=settings.docs_url,
    openapi_url=settings.openapi_url,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_router = APIRouter(prefix=settings.api_v1_prefix)
api_router.include_router(auth.router)
api_router.include_router(dashboard.router)
api_router.include_router(portal.router)
api_router.include_router(recruitment.router)
api_router.include_router(students.router)
api_router.include_router(training.router)
api_router.include_router(degree.router)
api_router.include_router(system.router)
api_router.include_router(workflow.router)
app.include_router(api_router)


@app.exception_handler(DatabaseUnavailableError)
async def handle_database_unavailable_error(request: Request, exc: DatabaseUnavailableError) -> Response:
    del request
    return Response(
        content=json.dumps({"detail": str(exc)}, ensure_ascii=False),
        status_code=503,
        media_type="application/json",
    )


def _should_proxy_frontend_path(path: str) -> bool:
    if not settings.frontend_dev_proxy_enabled:
        return False

    reserved_prefixes = (
        settings.api_v1_prefix,
        settings.docs_url,
        settings.openapi_url,
        "/health",
    )
    for prefix in reserved_prefixes:
        normalized_prefix = prefix.rstrip("/") or "/"
        if path == normalized_prefix or path.startswith(f"{normalized_prefix}/"):
            return False
    return True


def _build_frontend_proxy_url(path: str, query: str) -> str:
    base_url = settings.frontend_dev_proxy_target.rstrip("/")
    target_url = f"{base_url}{path}"
    if query:
        return f"{target_url}?{query}"
    return target_url


if settings.frontend_dev_proxy_enabled:
    @app.api_route("/", methods=["GET", "HEAD", "OPTIONS"], include_in_schema=False)
    @app.api_route("/{full_path:path}", methods=["GET", "HEAD", "OPTIONS"], include_in_schema=False)
    async def proxy_frontend_dev_server(request: Request, full_path: str = "") -> Response:
        path = f"/{full_path}" if full_path else "/"
        if not _should_proxy_frontend_path(path):
            raise HTTPException(status_code=404, detail="Not Found")

        proxy_headers = {
            key: value
            for key, value in request.headers.items()
            if key.lower() not in _HOP_BY_HOP_HEADERS
        }
        try:
            async with httpx.AsyncClient(timeout=settings.frontend_dev_proxy_timeout_seconds, trust_env=False) as client:
                upstream_response = await client.request(
                    request.method,
                    _build_frontend_proxy_url(path, request.url.query),
                    headers=proxy_headers,
                )
        except httpx.RequestError as exc:
            raise HTTPException(status_code=502, detail="Frontend dev server unavailable") from exc

        response_headers = {
            key: value
            for key, value in upstream_response.headers.items()
            if key.lower() not in _HOP_BY_HOP_HEADERS
        }
        return Response(
            content=upstream_response.content,
            status_code=upstream_response.status_code,
            headers=response_headers,
            media_type=upstream_response.headers.get("content-type"),
        )


@app.get("/health", tags=["system"])
def healthcheck() -> dict[str, str]:
    return {
        "status": "ok",
        "service": settings.app_name,
        "environment": settings.environment,
    }


@app.on_event("startup")
def on_startup() -> None:
    startup_begin = perf_counter()
    if settings.frontend_dev_proxy_enabled:
        logger.info("Frontend dev proxy enabled: %s", settings.frontend_dev_proxy_target)
    repair_result = repair_startup_postgres_state()
    logger.info(
        "Startup PostgreSQL repairs complete, renamed recruitment application keys: %s",
        repair_result["renamed_recruitment_application_keys"],
    )
    warmup_elapsed = warm_up_runtime_management_store()
    logger.info("Runtime management store warmed up in %.3fs", warmup_elapsed)
    logger.info("DTLMS backend startup complete in %.3fs", perf_counter() - startup_begin)
