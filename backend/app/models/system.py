from __future__ import annotations

from sqlalchemy import JSON, Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, SoftDeleteMixin, TimestampMixin


class User(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "dtlms_users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(128), nullable=False)
    email: Mapped[str | None] = mapped_column(String(128))
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class Role(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "dtlms_roles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    role_code: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    role_name: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)


class Permission(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "dtlms_permissions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    permission_code: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    permission_name: Mapped[str] = mapped_column(String(128), nullable=False)
    module_name: Mapped[str] = mapped_column(String(64), nullable=False)


class UserRole(Base, TimestampMixin):
    __tablename__ = "dtlms_user_roles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("dtlms_users.id"), nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("dtlms_roles.id"), nullable=False)
    grant_source: Mapped[str] = mapped_column(String(64), nullable=False, default="bootstrap")


class RolePermission(Base, TimestampMixin):
    __tablename__ = "dtlms_role_permissions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("dtlms_roles.id"), nullable=False)
    permission_id: Mapped[int] = mapped_column(ForeignKey("dtlms_permissions.id"), nullable=False)


class LoginLog(Base, TimestampMixin):
    __tablename__ = "dtlms_login_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(64), nullable=False)
    login_status: Mapped[str] = mapped_column(String(32), nullable=False)
    login_ip: Mapped[str | None] = mapped_column(String(64))
    user_agent: Mapped[str | None] = mapped_column(Text)


class OperationLog(Base, TimestampMixin):
    __tablename__ = "dtlms_operation_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    operator_username: Mapped[str] = mapped_column(String(64), nullable=False)
    operator_role: Mapped[str] = mapped_column(String(64), nullable=False)
    module_name: Mapped[str] = mapped_column(String(64), nullable=False)
    entity_name: Mapped[str] = mapped_column(String(64), nullable=False)
    entity_id: Mapped[str] = mapped_column(String(64), nullable=False)
    action: Mapped[str] = mapped_column(String(32), nullable=False)
    old_value: Mapped[dict | None] = mapped_column(JSON)
    new_value: Mapped[dict | None] = mapped_column(JSON)
    request_ip: Mapped[str | None] = mapped_column(String(64))
    result: Mapped[str] = mapped_column(String(32), nullable=False, default="success")


class DataSyncLog(Base, TimestampMixin):
    __tablename__ = "dtlms_data_sync_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    source_system: Mapped[str] = mapped_column(String(64), nullable=False)
    target_system: Mapped[str] = mapped_column(String(64), nullable=False)
    sync_status: Mapped[str] = mapped_column(String(32), nullable=False)
    record_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    failure_reason: Mapped[str | None] = mapped_column(Text)


class NotificationDeliveryLog(Base, TimestampMixin):
    __tablename__ = "dtlms_notification_delivery_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    channel: Mapped[str] = mapped_column(String(32), nullable=False)
    template_code: Mapped[str | None] = mapped_column(String(64))
    recipient: Mapped[str] = mapped_column(String(255), nullable=False)
    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    send_status: Mapped[str] = mapped_column(String(32), nullable=False)
    failure_reason: Mapped[str | None] = mapped_column(Text)
    business_key: Mapped[str | None] = mapped_column(String(64))
    triggered_by: Mapped[str | None] = mapped_column(String(64))


class NotificationTemplate(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "dtlms_notification_templates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    template_code: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    channel: Mapped[str] = mapped_column(String(32), nullable=False)
    title: Mapped[str] = mapped_column(String(128), nullable=False)
    content_template: Mapped[str] = mapped_column(Text, nullable=False)
    variables_schema: Mapped[dict | None] = mapped_column(JSON)


class SystemConfig(Base, TimestampMixin):
    __tablename__ = "dtlms_system_configs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    config_key: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    config_value: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)


class DictType(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "dtlms_dict_types"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    dict_name: Mapped[str] = mapped_column(String(100), nullable=False)
    dict_type: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="启用")
    remark: Mapped[str | None] = mapped_column(Text)


class DictData(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "dtlms_dict_data"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    dict_type_id: Mapped[int] = mapped_column(ForeignKey("dtlms_dict_types.id"), nullable=False)
    dict_type: Mapped[str] = mapped_column(String(100), nullable=False)
    label: Mapped[str] = mapped_column(String(100), nullable=False)
    value: Mapped[str] = mapped_column(String(100), nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="启用")
    color_type: Mapped[str | None] = mapped_column(String(32))
    css_class: Mapped[str | None] = mapped_column(String(128))
    remark: Mapped[str | None] = mapped_column(Text)
