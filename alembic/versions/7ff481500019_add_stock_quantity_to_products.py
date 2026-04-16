"""add stock_quantity to products

Revision ID: 7ff481500019
Revises: a330b771f76a
Create Date: 2026-04-16 20:03:08.164871

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7ff481500019"
down_revision: Union[str, Sequence[str], None] = "a330b771f76a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "products",
        sa.Column("stock_quantity", sa.Integer(), nullable=True),
    )
    op.execute(
        "UPDATE products SET stock_quantity = 0 WHERE stock_quantity IS NULL"
    )
    op.alter_column("products", "stock_quantity", nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("products", "stock_quantity")
