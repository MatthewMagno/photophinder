import uuid
from datetime import datetime

from sqlalchemy import JSON, TIMESTAMP, Column, ForeignKey, Table, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector

from ..config import settings
from ..db import Base


class Photo(Base):
    __tablename__ = "photos"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    original_key: Mapped[str] = mapped_column(Text, nullable=False)
    preview_key: Mapped[str] = mapped_column(Text, nullable=False)
    thumb_key: Mapped[str] = mapped_column(Text, nullable=False)
    caption: Mapped[str | None] = mapped_column(Text, nullable=True)
    objects: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
    taken_at: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow
    )

    embeddings: Mapped["PhotoEmbedding"] = relationship("PhotoEmbedding", back_populates="photo", uselist=False)
    faces: Mapped[list["Face"]] = relationship("Face", back_populates="photo")


class PhotoEmbedding(Base):
    __tablename__ = "photo_embeddings"

    photo_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("photos.id", ondelete="CASCADE"), primary_key=True
    )
    image_embedding: Mapped[list[float]] = mapped_column(Vector(settings.embeddings_dimension), nullable=False)
    caption_embedding: Mapped[list[float] | None] = mapped_column(Vector(settings.embeddings_dimension), nullable=True)

    photo: Mapped[Photo] = relationship("Photo", back_populates="embeddings")


class Person(Base):
    __tablename__ = "persons"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    display_name: Mapped[str] = mapped_column(Text, nullable=False)

    faces: Mapped[list["Face"]] = relationship("Face", back_populates="person")


class Face(Base):
    __tablename__ = "faces"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    photo_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("photos.id", ondelete="CASCADE"))
    person_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("persons.id"), nullable=True)
    embedding: Mapped[list[float]] = mapped_column(Vector(settings.embeddings_dimension), nullable=False)
    bounding_box: Mapped[dict] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)

    photo: Mapped[Photo] = relationship("Photo", back_populates="faces")
    person: Mapped[Person | None] = relationship("Person", back_populates="faces")


photo_persons = Table(
    "photo_persons",
    Base.metadata,
    Column("photo_id", UUID(as_uuid=True), ForeignKey("photos.id", ondelete="CASCADE"), primary_key=True),
    Column("person_id", UUID(as_uuid=True), ForeignKey("persons.id", ondelete="CASCADE"), primary_key=True),
)
