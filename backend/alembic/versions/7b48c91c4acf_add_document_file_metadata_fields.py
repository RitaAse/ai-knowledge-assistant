"""Add document file metadata fields

Revision ID: 7b48c91c4acf
Revises: 8e0745ea023a
Create Date: 2026-07-14 14:26:08.921574

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7b48c91c4acf'
down_revision: Union[str, Sequence[str], None] = '8e0745ea023a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "documents",
        sa.Column(
            "file_path",
            sa.String(),
            nullable=False,
            server_default="unknown",
        ),
    )

    op.add_column(
        "documents",
        sa.Column(
            "file_type",
            sa.String(),
            nullable=False,
            server_default="application/octet-stream",
        ),
    )

    op.add_column(
        "documents",
        sa.Column(
            "file_size",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
    )

    op.add_column(
        "documents",
        sa.Column(
            "processing_status",
            sa.String(),
            nullable=False,
            server_default="UPLOADED",
        ),
    )

    op.add_column(
        "documents",
        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )

    # Remove temporary defaults after existing rows are populated
    op.alter_column(
        "documents",
        "file_path",
        server_default=None,
    )

    op.alter_column(
        "documents",
        "file_type",
        server_default=None,
    )

    op.alter_column(
        "documents",
        "file_size",
        server_default=None,
    )

    op.alter_column(
        "documents",
        "processing_status",
        server_default=None,
    )

    op.alter_column(
        "documents",
        "updated_at",
        server_default=None,
    )