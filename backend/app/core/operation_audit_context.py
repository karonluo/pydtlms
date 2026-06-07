from contextvars import ContextVar, Token


_manual_operation_log_count: ContextVar[int] = ContextVar("manual_operation_log_count", default=0)


def begin_operation_audit_scope() -> Token[int]:
    return _manual_operation_log_count.set(0)


def end_operation_audit_scope(token: Token[int]) -> None:
    _manual_operation_log_count.reset(token)


def mark_manual_operation_log() -> None:
    _manual_operation_log_count.set(_manual_operation_log_count.get() + 1)


def has_manual_operation_log() -> bool:
    return _manual_operation_log_count.get() > 0