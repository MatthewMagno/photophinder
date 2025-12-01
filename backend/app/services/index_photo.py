import uuid
from typing import Optional
import io

from PIL import Image
from sqlalchemy.orm import Session

from .. import storage
from ..models import faces as face_models
from ..models import objects as object_models
from ..models import openclip, caption
from ..models import Face, Photo, PhotoEmbedding


def index_photo(db: Session, photo_id: uuid.UUID) -> None:
    photo: Optional[Photo] = db.query(Photo).filter(Photo.id == photo_id).first()
    if not photo:
        return

    # Download image bytes from storage
    # For demonstration, assume preview is sufficient
    import requests

    image_url = storage.generate_url(photo.preview_key)
    resp = requests.get(image_url)
    resp.raise_for_status()
    image = Image.open(io.BytesIO(resp.content)).convert("RGB")

    # Global embedding
    image_embedding = openclip.encode_image(image)

    # Captioning
    generated_caption = caption.generate_caption(image)
    caption_embedding = openclip.encode_text(generated_caption)

    # Object detection
    detected_objects = [obj["label"] for obj in object_models.detect_objects(image)]

    # Face detection & embeddings
    faces = []
    for box in face_models.detect_faces(image):
        cropped = image.crop((box.x1, box.y1, box.x2, box.y2))
        embedding = face_models.embed_face(cropped)
        faces.append(
            Face(
                photo_id=photo.id,
                embedding=embedding,
                bounding_box={"x1": box.x1, "y1": box.y1, "x2": box.x2, "y2": box.y2},
            )
        )

    # Persist data
    embedding_record = PhotoEmbedding(
        photo_id=photo.id,
        image_embedding=image_embedding,
        caption_embedding=caption_embedding,
    )
    photo.caption = generated_caption
    photo.objects = detected_objects
    db.add(embedding_record)
    for face in faces:
        db.add(face)
    db.commit()

