from celery import Celery
from datetime import timedelta

from app.core.config import settings
from app.scheduled_task_services.initial_screening_confirmation_service import send_initial_screening_confirmation_statistics


celery_app = Celery(
    "pydtlms",
    broker=settings.redis_url,
    backend=settings.redis_url,
)
celery_app.conf.broker_transport_options = settings.redis_celery_transport_options
celery_app.conf.result_backend_transport_options = settings.redis_celery_transport_options
celery_app.conf.task_default_queue = "dtlms-reminders"
celery_app.conf.timezone = "Asia/Shanghai"
celery_app.conf.beat_schedule = {
    "send-initial-screening-confirmation-statistics": {
        "task": "dtlms.send_initial_screening_confirmation_statistics",
        "schedule": timedelta(seconds=max(int(settings.initial_screening_confirmation_timeout_second or 0), 1)),
    }
}


@celery_app.task(name="dtlms.send_initial_screening_confirmation_statistics")
def send_initial_screening_confirmation_statistics_task() -> dict[str, object]:
    return send_initial_screening_confirmation_statistics()


@celery_app.task(name="dtlms.dispatch_deadline_reminder")
def dispatch_deadline_reminder(module_name: str, entity_code: str) -> dict[str, str]:
    return {
        "module": module_name,
        "entity": entity_code,
        "status": "queued",
    }
