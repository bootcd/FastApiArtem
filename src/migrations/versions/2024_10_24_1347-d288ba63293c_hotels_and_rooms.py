"""hotels and rooms

Revision ID: d288ba63293c
Revises: 
Create Date: 2024-10-24 13:47:46.830717

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "d288ba63293c"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_table("rooms")
    op.drop_table("hotels")

def downgrade() -> None:
    op.create_table(
        "hotels",
        sa.Column(
            "id",
            sa.INTEGER(),
            server_default=sa.text("nextval('hotels_id_seq'::regclass)"),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column("title", sa.VARCHAR(length=100), autoincrement=False, nullable=False),
        sa.Column("location", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint("id", name="hotels_pkey"),
        postgresql_ignore_search_path=False,
    )
    op.create_table(
        "rooms",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("hotel_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("title", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("description", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("quantity", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("price", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(
            ["hotel_id"], ["hotels.id"], name="rooms_hotel_id_fkey"
        ),
        sa.PrimaryKeyConstraint("id", name="rooms_pkey"),
    )
