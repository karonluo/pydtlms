import json
from time import perf_counter

import httpx
from fastapi import APIRouter, FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import auth, dashboard, degree, news, portal, recruitment, students, system, training, workflow
from app.core.config import settings
from app.core.exceptions import DatabaseUnavailableError
from app.core.logging import configure_logging
from app.core.security import decode_token
from app.services.management_service import store


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

_AUDIT_METHOD_TO_ACTION = {
    "POST": "新增",
    "PUT": "编辑",
    "PATCH": "编辑",
    "DELETE": "删除",
}

_AUDIT_MODULE_BY_SEGMENT = {
    "system": "系统治理",
    "students": "学生管理",
    "recruitment": "招生管理",
    "training": "培养管理",
    "degree": "学位管理",
    "workflow": "流程中心",
    "news": "招生宣传",
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
api_router.include_router(news.router)
api_router.include_router(portal.router)
api_router.include_router(recruitment.router)
api_router.include_router(students.router)
api_router.include_router(training.router)
api_router.include_router(degree.router)
api_router.include_router(system.router)
api_router.include_router(workflow.router)
app.include_router(api_router)


def _extract_bearer_token(request: Request) -> str | None:
    authorization = str(request.headers.get("authorization") or "").strip()
    if not authorization:
        return None
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        return None
    return token.strip()


def _resolve_operator_username(request: Request) -> str:
    token = _extract_bearer_token(request)
    if not token:
        return "anonymous"
    try:
        payload = decode_token(token)
    except Exception:
        return "anonymous"
    username = payload.get("sub")
    return str(username or "anonymous")


def _is_backoffice_write_request(request: Request) -> bool:
    if request.method.upper() not in _AUDIT_METHOD_TO_ACTION:
        return False

    prefix = settings.api_v1_prefix.rstrip("/")
    path = request.url.path
    if not path.startswith(f"{prefix}/"):
        return False

    excluded_prefixes = (
        f"{prefix}/portal",
        f"{prefix}/auth",
    )
    if any(path == item or path.startswith(f"{item}/") for item in excluded_prefixes):
        return False
    return True


def _resolve_audit_module_entity(path: str) -> tuple[str, str, str]:
    relative_path = path.removeprefix(settings.api_v1_prefix).strip("/")
    segments = [segment for segment in relative_path.split("/") if segment]
    if not segments:
        return "后台管理", "接口", "-"

    module_segment = segments[0]
    module_name = _AUDIT_MODULE_BY_SEGMENT.get(module_segment, "后台管理")
    entity_name = segments[1] if len(segments) > 1 else module_segment
    entity_id = "/".join(segments[2:]) if len(segments) > 2 else "-"
    return module_name, entity_name, entity_id


def _resolve_business_audit_descriptor(request: Request) -> tuple[str, str, str, str, str] | None:
    prefix = settings.api_v1_prefix.rstrip("/")
    path = request.url.path
    method = request.method.upper()

    if method == "POST" and path == f"{prefix}/students/portal-registrations/export-jobs":
        return "学生管理", "注册学生", "-", "导出", "导出注册学生"

    news_prefix = f"{prefix}/recruitment/news/"
    if method == "POST" and path.startswith(news_prefix) and path.endswith("/publish"):
        entity_id = path[len(news_prefix):-len("/publish")].strip("/") or "-"
        return "招生宣传", "新闻", entity_id, "发布", "发布新闻"

    if method == "POST" and path == f"{prefix}/recruitment/news/batch-publish":
        return "招生宣传", "新闻", "批量", "发布", "批量发布新闻"

    return None


@app.middleware("http")
async def record_backoffice_operation_audit(request: Request, call_next):
    should_audit = _is_backoffice_write_request(request)
    operation_log_count_before = int(getattr(store, "_counters", {}).get("operation_logs", 0)) if should_audit else 0
    started_at = perf_counter()
    status_code = 500
    response: Response | None = None
    raised_exc: Exception | None = None

    try:
        response = await call_next(request)
        status_code = response.status_code
        return response
    except Exception as exc:
        raised_exc = exc
        raise
    finally:
        if should_audit:
            operation_log_count_after = int(getattr(store, "_counters", {}).get("operation_logs", 0))
            if operation_log_count_after <= operation_log_count_before:
                elapsed_ms = round((perf_counter() - started_at) * 1000, 2)
                business_descriptor = _resolve_business_audit_descriptor(request)
                if business_descriptor is None:
                    module_name, entity_name, entity_id = _resolve_audit_module_entity(request.url.path)
                    action = _AUDIT_METHOD_TO_ACTION.get(request.method.upper(), "操作")
                    summary = f"管理端接口 {request.method.upper()} {request.url.path}；状态码 {status_code}；耗时 {elapsed_ms} ms"
                else:
                    module_name, entity_name, entity_id, action, summary = business_descriptor
                result = "success" if status_code < 400 and raised_exc is None else "failed"
                operator_username = _resolve_operator_username(request)

                try:
                    store.record_operation_event(
                        module_name,
                        entity_name,
                        entity_id,
                        action,
                        summary,
                        operator_username=operator_username,
                        result=result,
                    )
                except Exception as exc:
                    logger.warning("Record backoffice operation audit failed: %s", exc)


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
    logger.info("Runtime management store will initialize lazily on first use; startup does not warm or persist runtime state")
    logger.info("DTLMS backend startup complete in %.3fs", perf_counter() - startup_begin)
