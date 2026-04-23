from pathlib import Path, PurePosixPath

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.main import app


FRONTEND_DIST_DIR = Path(__file__).resolve().parents[2] / "frontend" / "dist"
FRONTEND_PUBLIC_DIR = Path(__file__).resolve().parents[2] / "frontend" / "public"
PORTAL_ATTACHMENTS_DIR = FRONTEND_PUBLIC_DIR / "portal-attachments"
PORTAL_BROCHURES_DIR = FRONTEND_PUBLIC_DIR / "portal-brochures"


class SPAStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope):  # type: ignore[override]
        try:
            return await super().get_response(path, scope)
        except StarletteHTTPException as exc:
            if exc.status_code != 404:
                raise

        requested_path = PurePosixPath(path)
        if requested_path.suffix:
            raise StarletteHTTPException(status_code=404)

        return await super().get_response("index.html", scope)


@app.get("/favicon.ico", include_in_schema=False)
def favicon() -> FileResponse:
    favicon_path = FRONTEND_DIST_DIR / "favicon.svg"
    return FileResponse(favicon_path)


def configure_static_frontend(target_app: FastAPI) -> None:
    if not FRONTEND_DIST_DIR.exists():
        return

    if PORTAL_ATTACHMENTS_DIR.exists():
        target_app.mount(
            "/portal-attachments",
            StaticFiles(directory=PORTAL_ATTACHMENTS_DIR),
            name="portal-attachments",
        )

    if PORTAL_BROCHURES_DIR.exists():
        target_app.mount(
            "/portal-brochures",
            StaticFiles(directory=PORTAL_BROCHURES_DIR),
            name="portal-brochures",
        )

    target_app.mount(
        "/",
        SPAStaticFiles(directory=FRONTEND_DIST_DIR, html=True),
        name="frontend-dist",
    )


configure_static_frontend(app)
