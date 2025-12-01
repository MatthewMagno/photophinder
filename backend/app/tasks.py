import uuid

from celery import Celery
from sqlalchemy.orm import Session

from .config import settings
from .db import SessionLocal
from .services.index_photo import index_photo

celery_app = Celery(
    "photophinder",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)


@celery_app.task
def process_photo(photo_id: str) -> None:
    with SessionLocal() as db:
        index_photo(db, uuid.UUID(photo_id))
