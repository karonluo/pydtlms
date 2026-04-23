from celery import Celery

from app.core.config import settings


celery_app = Celery(
    "pydtlms",
    broker=settings.redis_url,
    backend=settings.redis_url,
)
celery_app.conf.broker_transport_options = settings.redis_celery_transport_options
celery_app.conf.result_backend_transport_options = settings.redis_celery_transport_options
celery_app.conf.task_default_queue = "dtlms-reminders"
celery_app.conf.timezone = "Asia/Shanghai"


@celery_app.task(name="dtlms.dispatch_deadline_reminder")
def dispatch_deadline_reminder(module_name: str, entity_code: str) -> dict[str, str]:
    return {
        "module": module_name,
        "entity": entity_code,
        "status": "queued",
    }
