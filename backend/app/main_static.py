from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.main import app


FRONTEND_DIST_DIR = Path(__file__).resolve().parents[2] / "frontend" / "dist"


class SPAStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope):  # type: ignore[override]
        try:
            return await super().get_response(path, scope)
        except HTTPException as exc:
            if exc.status_code != 404:
                raise

        return await super().get_response("index.html", scope)


@app.get("/favicon.ico", include_in_schema=False)
def favicon() -> FileResponse:
    favicon_path = FRONTEND_DIST_DIR / "favicon.svg"
    return FileResponse(favicon_path)


def configure_static_frontend(target_app: FastAPI) -> None:
    if not FRONTEND_DIST_DIR.exists():
        return

    target_app.mount(
        "/",
        SPAStaticFiles(directory=FRONTEND_DIST_DIR, html=True),
        name="frontend-dist",
    )


configure_static_frontend(app)
