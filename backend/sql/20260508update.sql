CREATE TABLE IF NOT EXISTS dtlms_notification_delivery_logs (
    id BIGSERIAL PRIMARY KEY,
    channel VARCHAR(32) NOT NULL,
    template_code VARCHAR(64),
    recipient VARCHAR(255) NOT NULL,
    subject VARCHAR(255) NOT NULL,
    send_status VARCHAR(32) NOT NULL,
    failure_reason TEXT,
    business_key VARCHAR(64),
    triggered_by VARCHAR(64),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_notification_delivery_logs_status_time
    ON dtlms_notification_delivery_logs(send_status, created_at);

CREATE INDEX IF NOT EXISTS idx_notification_delivery_logs_channel_time
    ON dtlms_notification_delivery_logs(channel, created_at);

CREATE INDEX IF NOT EXISTS idx_notification_delivery_logs_recipient
    ON dtlms_notification_delivery_logs(recipient);