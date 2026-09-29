from celery import Celery

from app.config import settings

celery_app = Celery(
    "namaa",
    broker=settings.redis_url,
    backend=settings.redis_url,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_default_queue="default",
)

# Task modules are registered here as they land in later phases
# (process_message, generate_ai_response, send_webhook, retention_cleanup, ...)
