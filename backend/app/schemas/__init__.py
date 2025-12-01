import uuid
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class PhotoCreate(BaseModel):
    taken_at: Optional[datetime] = None


class PhotoResponse(BaseModel):
    id: uuid.UUID
    original_key: str
    preview_key: str
    thumb_key: str
    caption: Optional[str]
    objects: Optional[list[str]]
    taken_at: Optional[datetime]
    created_at: datetime

    class Config:
        orm_mode = True


class FaceResponse(BaseModel):
    id: uuid.UUID
    bounding_box: dict
    person_name: Optional[str] = Field(default=None, alias="person")

    class Config:
        allow_population_by_field_name = True
        orm_mode = True


class PhotoDetailResponse(PhotoResponse):
    faces: List[FaceResponse]


class FaceLabelRequest(BaseModel):
    display_name: str


class SearchResponse(BaseModel):
    id: uuid.UUID
    thumb_key: str
    preview_key: str
    caption: Optional[str]

    class Config:
        orm_mode = True
