"""add equipment indexes

Revision ID: 4476f877dd0f
Revises: bf015c392cda
Create Date: 2025-08-12 16:50:16.472595

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "4476f877dd0f"
down_revision: str | Sequence[str] | None = "bf015c392cda"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_index("ix_equipment_name", "equipment", ["name"])
    op.create_index("ix_equipment_type", "equipment", ["type"])
    op.create_index("ix_equipment_serial_number", "equipment", ["serial_number"])
    op.create_index("ix_equipment_inventory_number", "equipment", ["inventory_number"])


def downgrade() -> None:
    op.drop_index("ix_equipment_inventory_number", table_name="equipment")
    op.drop_index("ix_equipment_serial_number", table_name="equipment")
    op.drop_index("ix_equipment_type", table_name="equipment")
    op.drop_index("ix_equipment_name", table_name="equipment")
