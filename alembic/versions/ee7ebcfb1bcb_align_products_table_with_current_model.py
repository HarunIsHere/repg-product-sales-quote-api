"""align products table with current model

Revision ID: ee7ebcfb1bcb
Revises: c481b96c5b06
Create Date: 2026-04-05 15:11:40.188182

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "ee7ebcfb1bcb"
down_revision: Union[str, Sequence[str], None] = "c481b96c5b06"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('CREATE EXTENSION IF NOT EXISTS "pgcrypto";')

    # Recreate products in the new structure
    op.execute("DROP TABLE IF EXISTS product_application_areas CASCADE")
    op.execute("DROP TABLE IF EXISTS ai_analysis CASCADE")
    op.execute("DROP TABLE IF EXISTS quote_requests CASCADE")
    op.execute("DROP TABLE IF EXISTS order_items CASCADE")
    op.execute("DROP TABLE IF EXISTS spare_parts CASCADE")
    op.execute("DROP TABLE IF EXISTS products CASCADE")
    
    

    op.create_table(
        "products",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("price", sa.Numeric(12, 2), nullable=False),
        sa.Column("currency", sa.String(), nullable=False),
        sa.Column("sku", sa.String(), nullable=False, unique=True),
        sa.Column("category", sa.String(), nullable=False),
        sa.Column("subcategory", sa.String(), nullable=False),
        sa.Column("product_type", sa.String(), nullable=False),
        sa.Column("stock_status", sa.String(), nullable=False),
        sa.Column("lead_time", sa.String(), nullable=False),
        sa.Column(
            "technical_specs",
            postgresql.JSON(astext_type=sa.Text()),
            nullable=False,
        ),
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("true"),
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=True,
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=True,
            server_default=sa.text("now()"),
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("products")

    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("slug", sa.String(length=220), nullable=False),
        sa.Column("category", sa.String(length=100), nullable=False),
        sa.Column("short_description", sa.String(length=300), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("price", sa.Numeric(10, 2), nullable=True),
        sa.Column("catalog_url", sa.Text(), nullable=True),
        sa.Column("daily_water_output_liters", sa.Numeric(10, 2), nullable=True),
        sa.Column("min_power_output_kwh", sa.Numeric(10, 2), nullable=True),
        sa.Column("max_power_output_kwh", sa.Numeric(10, 2), nullable=True),
        sa.Column(
            "min_operating_temperature_c",
            sa.Numeric(6, 2),
            nullable=True,
        ),
        sa.Column(
            "max_operating_temperature_c",
            sa.Numeric(6, 2),
            nullable=True,
        ),
        sa.Column("portable", sa.Boolean(), nullable=False),
        sa.Column("off_grid_capable", sa.Boolean(), nullable=False),
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("true"),
        ),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "updated_at",
            postgresql.TIMESTAMP(),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )

    op.create_index(op.f("ix_products_id"), "products", ["id"], unique=False)
    op.create_index(op.f("ix_products_slug"), "products", ["slug"], unique=True)
