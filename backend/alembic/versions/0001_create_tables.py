"""initial schema"""
from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
    op.execute('CREATE EXTENSION IF NOT EXISTS "vector";')

    op.create_table(
        "photos",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("original_key", sa.Text(), nullable=False),
        sa.Column("preview_key", sa.Text(), nullable=False),
        sa.Column("thumb_key", sa.Text(), nullable=False),
        sa.Column("caption", sa.Text(), nullable=True),
        sa.Column("objects", sa.JSON(), nullable=True),
        sa.Column("taken_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")),
    )

    op.create_table(
        "photo_embeddings",
        sa.Column("photo_id", sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey("photos.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("image_embedding", Vector(512), nullable=False),
        sa.Column("caption_embedding", Vector(512), nullable=True),
    )

    op.create_table(
        "persons",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("display_name", sa.Text(), nullable=False),
    )

    op.create_table(
        "faces",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("photo_id", sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey("photos.id", ondelete="CASCADE")),
        sa.Column("person_id", sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey("persons.id"), nullable=True),
        sa.Column("embedding", Vector(512), nullable=False),
        sa.Column("bounding_box", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")),
    )

    op.create_table(
        "photo_persons",
        sa.Column("photo_id", sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey("photos.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("person_id", sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey("persons.id", ondelete="CASCADE"), primary_key=True),
    )


def downgrade():
    op.drop_table("photo_persons")
    op.drop_table("faces")
    op.drop_table("persons")
    op.drop_table("photo_embeddings")
    op.drop_table("photos")
