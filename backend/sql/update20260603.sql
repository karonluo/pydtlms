-- 2026-06-03 新闻信息管理数据库补丁
-- 说明：新增新闻类型字典与新闻信息表，为新闻管理后台提供数据基础。

BEGIN;

INSERT INTO dtlms_dict_types (dict_name, dict_type, status, remark)
VALUES
    ('新闻类型', 'news_type', '启用', '新闻类型字典')
ON CONFLICT (dict_type) DO UPDATE
SET dict_name = EXCLUDED.dict_name,
    status = EXCLUDED.status,
    remark = EXCLUDED.remark,
    updated_at = CURRENT_TIMESTAMP,
    is_deleted = FALSE;

WITH seed_data(dict_type, label, value, sort_order, status, color_type, css_class, remark) AS (
    VALUES
        ('news_type', '学生门户通知消息', '学生门户通知消息', 10, '启用', NULL, NULL, '面向学生门户的通知类消息'),
        ('news_type', '学生门户新闻信息', '学生门户新闻信息', 20, '启用', NULL, NULL, '面向学生门户的新闻类信息')
)
INSERT INTO dtlms_dict_data (dict_type_id, dict_type, label, value, sort_order, status, color_type, css_class, remark)
SELECT t.id, s.dict_type, s.label, s.value, s.sort_order, s.status, s.color_type, s.css_class, s.remark
FROM seed_data s
JOIN dtlms_dict_types t ON t.dict_type = s.dict_type
ON CONFLICT (dict_type, value) DO UPDATE SET
    dict_type_id = EXCLUDED.dict_type_id,
    label = EXCLUDED.label,
    sort_order = EXCLUDED.sort_order,
    status = EXCLUDED.status,
    color_type = EXCLUDED.color_type,
    css_class = EXCLUDED.css_class,
    remark = EXCLUDED.remark,
    updated_at = CURRENT_TIMESTAMP,
    is_deleted = FALSE;

COMMIT;

BEGIN;

CREATE TABLE IF NOT EXISTS dtlms_news_articles (
    id BIGSERIAL PRIMARY KEY,
    news_code VARCHAR(64) NOT NULL UNIQUE,
    news_title VARCHAR(255) NOT NULL,
    news_content TEXT NOT NULL,
    news_type VARCHAR(100) NOT NULL,
    publisher_user_id BIGINT,
    publisher_username VARCHAR(64),
    publisher_name VARCHAR(128),
    reviewer_user_id BIGINT,
    reviewer_username VARCHAR(64),
    reviewer_name VARCHAR(128),
    published_at TIMESTAMPTZ,
    status VARCHAR(32) NOT NULL DEFAULT '草稿',
    is_pinned BOOLEAN NOT NULL DEFAULT FALSE,
    display_order INTEGER NOT NULL DEFAULT 0,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_dtlms_news_articles_status CHECK (status IN ('草稿', '待发布', '已发布', '已下线')),
    CONSTRAINT chk_dtlms_news_articles_type CHECK (news_type IN ('学生门户通知消息', '学生门户新闻信息'))
);

CREATE INDEX IF NOT EXISTS idx_dtlms_news_articles_status_published
    ON dtlms_news_articles (status, published_at DESC, display_order DESC, id DESC)
    WHERE is_deleted = FALSE;

CREATE INDEX IF NOT EXISTS idx_dtlms_news_articles_type_status
    ON dtlms_news_articles (news_type, status, published_at DESC, id DESC)
    WHERE is_deleted = FALSE;

CREATE INDEX IF NOT EXISTS idx_dtlms_news_articles_deleted_order
    ON dtlms_news_articles (is_deleted, display_order DESC, id DESC);

COMMIT;