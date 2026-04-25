from celery import Celery

from .config.settings import settings


celery_app = Celery(
    "template",
    broker=settings.celery_broker_url,
    backend=settings.redis_url,
)

# Basic defaults
celery_app.conf.task_default_queue = "default"
celery_app.conf.task_default_retry_delay = 60  # seconds
celery_app.conf.task_default_max_retries = 3
celery_app.conf.task_acks_late = True
celery_app.conf.worker_prefetch_multiplier = 1
celery_app.conf.broker_connection_retry = True
celery_app.conf.broker_connection_max_retries = 10

# Autodiscover tasks in common locations; add your tasks under src.app.tasks
try:
    celery_app.autodiscover_tasks(["src.app.tasks", "src.app"])
except Exception:
    # If no tasks package exists yet, continue silently.
    pass


@celery_app.task(name="template.ping")
def ping():
    return "pong"
