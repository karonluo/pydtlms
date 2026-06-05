from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status

from app.core.rbac import require_permissions
from app.schemas.auth import Principal
from app.schemas.common import SelectOption
from app.schemas.system import BulkActionResponse, BulkDeleteRequest
from app.schemas.news import NewsArticleListResponse, NewsArticleRecord, NewsArticleUpsert, NewsImageUploadResponse
from app.services.dashboard_service import (
    batch_offline_news_articles,
    batch_publish_news_articles,
    create_news_article,
    delete_news_article,
    get_news_article_detail,
    get_news_article_list,
    get_news_type_options,
    offline_news_article,
    publish_news_article,
    update_news_article,
)


router = APIRouter(prefix="/recruitment/news", tags=["news"])
PROJECT_ROOT = Path(__file__).resolve().parents[4]
NEWS_UPLOAD_DIR = PROJECT_ROOT / "frontend" / "public" / "recruitment" / "news" / "uploads"


@router.get("/options/news-types", response_model=list[SelectOption])
def news_type_options(principal: Principal = Depends(require_permissions("news_management:read"))) -> list[SelectOption]:
    return get_news_type_options()


@router.get("", response_model=NewsArticleListResponse)
def news_articles(
    keyword: str | None = Query(default=None),
    news_type: str | None = Query(default=None),
    status_filter: str | None = Query(default=None, alias="status"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=1000),
    principal: Principal = Depends(require_permissions("news_management:read")),
) -> NewsArticleListResponse:
    return get_news_article_list(keyword=keyword, news_type=news_type, status=status_filter, page=page, page_size=page_size)


@router.get("/{news_article_id}", response_model=NewsArticleRecord)
def news_article_detail(news_article_id: int, principal: Principal = Depends(require_permissions("news_management:read"))) -> NewsArticleRecord:
    try:
        return get_news_article_detail(news_article_id)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="News article not found") from exc


@router.post("", response_model=NewsArticleRecord, status_code=status.HTTP_201_CREATED)
def create_news_article_record(payload: NewsArticleUpsert, principal: Principal = Depends(require_permissions("recruitment:write"))) -> NewsArticleRecord:
    try:
        return create_news_article(payload, principal=principal)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.put("/{news_article_id}", response_model=NewsArticleRecord)
def update_news_article_record(news_article_id: int, payload: NewsArticleUpsert, principal: Principal = Depends(require_permissions("recruitment:write"))) -> NewsArticleRecord:
    try:
        return update_news_article(news_article_id, payload, principal=principal)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="News article not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{news_article_id}/publish", response_model=NewsArticleRecord)
def publish_news_article_record(news_article_id: int, principal: Principal = Depends(require_permissions("recruitment:write"))) -> NewsArticleRecord:
    try:
        return publish_news_article(news_article_id, principal=principal)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="News article not found") from exc


@router.post("/{news_article_id}/offline", response_model=NewsArticleRecord)
def offline_news_article_record(news_article_id: int, principal: Principal = Depends(require_permissions("recruitment:write"))) -> NewsArticleRecord:
    try:
        return offline_news_article(news_article_id)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="News article not found") from exc


@router.post("/batch-publish", response_model=BulkActionResponse)
def batch_publish_news_article_records(payload: BulkDeleteRequest, principal: Principal = Depends(require_permissions("recruitment:write"))) -> BulkActionResponse:
    return batch_publish_news_articles(payload.ids, principal=principal)


@router.post("/batch-offline", response_model=BulkActionResponse)
def batch_offline_news_article_records(payload: BulkDeleteRequest, principal: Principal = Depends(require_permissions("recruitment:write"))) -> BulkActionResponse:
    return batch_offline_news_articles(payload.ids)


@router.delete("/{news_article_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_news_article_record(news_article_id: int, principal: Principal = Depends(require_permissions("recruitment:write"))) -> None:
    try:
        delete_news_article(news_article_id)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="News article not found") from exc


@router.post("/image-upload", response_model=NewsImageUploadResponse)
async def upload_news_image(file: UploadFile = File(...), principal: Principal = Depends(require_permissions("recruitment:write"))) -> NewsImageUploadResponse:
    content_type = str(file.content_type or "")
    if not content_type.startswith("image/"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="仅支持上传图片文件")

    suffix = Path(file.filename or "image.png").suffix.lower() or ".png"
    if suffix not in {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"}:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="图片格式不受支持")

    NEWS_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"news-{uuid4().hex}{suffix}"
    target = NEWS_UPLOAD_DIR / filename
    target.write_bytes(await file.read())
    return NewsImageUploadResponse(url=f"/recruitment/news/uploads/{filename}")