from __future__ import annotations

from time import perf_counter

from .management_service_shared import Any, Lock, NotificationEmailService, PostgresStateStore, get_cache_client
from .management_service_core import RuntimeManagementStoreCoreMixin
from .management_service_workflow import RuntimeManagementStoreWorkflowMixin
from .management_service_portal import RuntimeManagementStorePortalMixin
from .management_service_recruitment import RuntimeManagementStoreRecruitmentMixin
from .management_service_students import RuntimeManagementStoreStudentsMixin
from .management_service_academic import RuntimeManagementStoreAcademicMixin
from .management_service_system import RuntimeManagementStoreSystemMixin


class RuntimeManagementStore(
    RuntimeManagementStoreSystemMixin,
    RuntimeManagementStoreAcademicMixin,
    RuntimeManagementStoreStudentsMixin,
    RuntimeManagementStoreRecruitmentMixin,
    RuntimeManagementStorePortalMixin,
    RuntimeManagementStoreWorkflowMixin,
    RuntimeManagementStoreCoreMixin,
):
    def _create_postgres_store(self):
        return PostgresStateStore()

    def _create_email_service(self):
        return NotificationEmailService(log_delivery=self._record_notification_delivery_log)

    def _get_cache_client(self):
        return get_cache_client()


class LazyRuntimeManagementStore:
    def __init__(self) -> None:
        self._instance: RuntimeManagementStore | None = None
        self._instance_lock = Lock()

    def _get_instance(self) -> RuntimeManagementStore:
        if self._instance is None:
            with self._instance_lock:
                if self._instance is None:
                    self._instance = RuntimeManagementStore()
        return self._instance

    def __getattr__(self, name: str) -> Any:
        return getattr(self._get_instance(), name)


store = LazyRuntimeManagementStore()


def repair_startup_postgres_state() -> dict[str, int]:
    postgres_store = PostgresStateStore()
    renamed_recruitment_application_keys = postgres_store.normalize_recruitment_application_business_keys()
    return {
        "renamed_recruitment_application_keys": renamed_recruitment_application_keys,
    }


def warm_up_runtime_management_store() -> float:
    start = perf_counter()
    store._get_instance()
    return perf_counter() - start


