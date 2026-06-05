from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.common import PaginationResponseBase


class NewsArticleRecord(BaseModel):
    id: int
    news_code: str
    news_title: str
    news_content: str
    news_type: str
    publisher_user_id: int | None = None
    publisher_username: str | None = None
    publisher_name: str | None = None
    reviewer_user_id: int | None = None
    reviewer_username: str | None = None
    reviewer_name: str | None = None
    published_at: datetime | None = None
    status: str
    is_pinned: bool
    display_order: int
    created_at: datetime
    updated_at: datetime


class NewsArticleUpsert(BaseModel):
    news_title: str = Field(min_length=1, max_length=255)
    news_content: str = Field(min_length=1)
    news_type: str = Field(min_length=1, max_length=100)
    published_at: datetime | None = None
    status: str = Field(default="草稿")
    is_pinned: bool = False
    display_order: int = 0


class NewsArticleListResponse(PaginationResponseBase):
    items: list[NewsArticleRecord]


class NewsImageUploadResponse(BaseModel):
    url: str