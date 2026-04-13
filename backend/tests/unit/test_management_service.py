from app.services.management_service import LazyRuntimeManagementStore


class FakeRuntimeManagementStore:
    init_count = 0

    def __init__(self) -> None:
        type(self).init_count += 1
        self.label = "runtime-store"

    def ping(self) -> str:
        return self.label


def test_lazy_store_does_not_create_instance_until_attribute_access(monkeypatch) -> None:
    FakeRuntimeManagementStore.init_count = 0
    monkeypatch.setattr("app.services.management_service.RuntimeManagementStore", FakeRuntimeManagementStore)

    store = LazyRuntimeManagementStore()

    assert FakeRuntimeManagementStore.init_count == 0
    assert store._instance is None


def test_lazy_store_reuses_single_runtime_instance(monkeypatch) -> None:
    FakeRuntimeManagementStore.init_count = 0
    monkeypatch.setattr("app.services.management_service.RuntimeManagementStore", FakeRuntimeManagementStore)

    store = LazyRuntimeManagementStore()

    assert store.ping() == "runtime-store"
    assert store.label == "runtime-store"
    assert FakeRuntimeManagementStore.init_count == 1