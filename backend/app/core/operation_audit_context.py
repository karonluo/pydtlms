from contextvars import ContextVar, Token
from typing import Any


_manual_operation_log_count: ContextVar[int] = ContextVar("manual_operation_log_count", default=0)
_operation_audit_context: ContextVar[dict[str, Any]] = ContextVar(
    "operation_audit_context", default={},
)


def begin_operation_audit_scope() -> Token[int]:
    return _manual_operation_log_count.set(0)


def end_operation_audit_scope(token: Token[int]) -> None:
    _manual_operation_log_count.reset(token)


def mark_manual_operation_log() -> None:
    _manual_operation_log_count.set(_manual_operation_log_count.get() + 1)


def has_manual_operation_log() -> bool:
    return _manual_operation_log_count.get() > 0


# === 操作审计上下文（步骤 1 扩展）===
# 用于在请求处理过程中，由中间件/业务代码写入，提交审计日志时一并读取。
# 支持的 key：
#   - request_payload: dict | None  - 请求体 JSON（已脱敏）
#   - old_value: dict | None        - 修改前快照（业务手工传入）
#   - new_value: dict | None        - 修改后快照（业务手工传入）
#   - request_ip: str | None        - 客户端 IP
#   - status_code: int | None       - 响应/异常 HTTP 状态码
#   - elapsed_ms: float | None      - 请求处理耗时（毫秒）
#   - error_detail: dict | None     - 失败详情（HTTPException/RequestValidationError/Exception）


def get_audit_context() -> dict[str, Any]:
    """获取当前请求的审计上下文快照（拷贝，避免调用方修改影响源数据）。"""
    return dict(_operation_audit_context.get())


def set_audit_context_value(key: str, value: Any) -> None:
    """在当前上下文中写入一个审计字段。"""
    current = dict(_operation_audit_context.get())
    current[key] = value
    _operation_audit_context.set(current)


def update_audit_context(values: dict[str, Any]) -> None:
    """批量合并字段到审计上下文。"""
    if not values:
        return
    current = dict(_operation_audit_context.get())
    current.update(values)
    _operation_audit_context.set(current)


def clear_audit_context() -> None:
    """清空当前审计上下文（一般请求结束时调用）。"""
    _operation_audit_context.set({})
