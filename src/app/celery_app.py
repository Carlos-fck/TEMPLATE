from celery import Celery

from .config.settings import settings


celery_app = Celery(
    "template",
    broker=settings.celery_broker_url,
    backend=settings.redis_url,
)

celery_app.conf.task_default_queue = "default"


@celery_app.task(name="template.ping")
def ping():
    return "pong"
