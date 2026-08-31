"""adiciona perfil ao usuario

Revision ID: a2b3c4d5e6f7
Revises: f9a2b3c4d5e6
Create Date: 2026-08-30 10:05:00

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "a2b3c4d5e6f7"
down_revision: str | Sequence[str] | None = "f9a2b3c4d5e6"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    perfil = postgresql.ENUM(
        "MANOBRADOR",
        "INSTRUTOR",
        "MONITOR_QUALIDADE",
        name="perfilusuario",
    )
    perfil.create(op.get_bind(), checkfirst=True)
    op.add_column(
        "usuario",
        sa.Column(
            "perfil",
            postgresql.ENUM(name="perfilusuario", create_type=False),
            nullable=False,
            server_default="MANOBRADOR",
        ),
    )


def downgrade() -> None:
    op.execute("UPDATE usuario SET perfil = 'MANOBRADOR' WHERE perfil <> 'MANOBRADOR'")
    op.drop_column("usuario", "perfil")
    postgresql.ENUM(name="perfilusuario").drop(op.get_bind(), checkfirst=True)
