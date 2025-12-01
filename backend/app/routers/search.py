from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Photo, PhotoEmbedding
from ..models import openclip
from ..schemas import SearchResponse

router = APIRouter(prefix="/search", tags=["search"])


@router.get("", response_model=List[SearchResponse])
def search_photos(query: str = Query(""), limit: int = 50, db: Session = Depends(get_db)):
    if not query:
        photos = db.query(Photo).order_by(Photo.created_at.desc()).limit(limit).all()
        return photos

    embedding = openclip.encode_text(query)
    results = (
        db.query(Photo)
        .join(PhotoEmbedding, PhotoEmbedding.photo_id == Photo.id)
        .order_by(PhotoEmbedding.image_embedding.op("<->")(embedding))
        .limit(limit)
        .all()
    )
    return results
