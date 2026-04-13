from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import auth, dashboard, degree, portal, recruitment, students, system, training, workflow
from app.core.config import settings
from app.core.logging import configure_logging


logger = configure_logging()

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


@app.get("/health", tags=["system"])
def healthcheck() -> dict[str, str]:
    return {
        "status": "ok",
        "service": settings.app_name,
        "environment": settings.environment,
    }


@app.on_event("startup")
def on_startup() -> None:
    logger.info("DTLMS backend startup complete")
