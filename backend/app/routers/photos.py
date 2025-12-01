import io
import uuid
from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from PIL import Image
from sqlalchemy.orm import Session

from .. import storage
from ..db import get_db
from ..models import Photo
from ..schemas import PhotoDetailResponse, PhotoResponse
from ..tasks import process_photo

router = APIRouter(prefix="/photos", tags=["photos"])


@router.post("/upload", response_model=PhotoResponse)
def upload_photo(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if file.content_type is None or not file.content_type.startswith("image"):
        raise HTTPException(status_code=400, detail="File must be an image")

    image_bytes = file.file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    # Generate preview and thumbnail
    preview = image.copy()
    preview.thumbnail((1280, 1280))
    thumb = image.copy()
    thumb.thumbnail((320, 320))

    buf_preview = io.BytesIO()
    preview.save(buf_preview, format="JPEG")
    buf_thumb = io.BytesIO()
    thumb.save(buf_thumb, format="JPEG")

    original_key = storage.build_key("original", ".jpg")
    preview_key = storage.build_key("preview", ".jpg")
    thumb_key = storage.build_key("thumb", ".jpg")

    storage.upload_file(image_bytes, original_key)
    storage.upload_file(buf_preview.getvalue(), preview_key)
    storage.upload_file(buf_thumb.getvalue(), thumb_key)

    photo = Photo(
        original_key=original_key,
        preview_key=preview_key,
        thumb_key=thumb_key,
    )
    db.add(photo)
    db.commit()
    db.refresh(photo)

    process_photo.delay(str(photo.id))

    return photo


@router.get("", response_model=List[PhotoResponse])
def list_photos(db: Session = Depends(get_db), limit: int = 50, offset: int = 0):
    return db.query(Photo).order_by(Photo.created_at.desc()).offset(offset).limit(limit).all()


@router.get("/{photo_id}", response_model=PhotoDetailResponse)
def get_photo(photo_id: uuid.UUID, db: Session = Depends(get_db)):
    photo = db.query(Photo).filter(Photo.id == photo_id).first()
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    return photo
