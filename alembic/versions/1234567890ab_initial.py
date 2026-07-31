"""initial

Revision ID: 1234567890ab
Revises: 
Create Date: 2026-07-31 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1234567890ab'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('eventos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(), nullable=True),
    sa.Column('ubicacion', sa.String(), nullable=True),
    sa.Column('capacidad', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_eventos_id'), 'eventos', ['id'], unique=False)
    op.create_index(op.f('ix_eventos_nombre'), 'eventos', ['nombre'], unique=False)

    op.create_table('boletos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('evento_id', sa.Integer(), nullable=True),
    sa.Column('nombre_comprador', sa.String(), nullable=True),
    sa.Column('pagado', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_boletos_evento_id'), 'boletos', ['evento_id'], unique=False)
    op.create_index(op.f('ix_boletos_id'), 'boletos', ['id'], unique=False)
    op.create_index(op.f('ix_boletos_nombre_comprador'), 'boletos', ['nombre_comprador'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_boletos_nombre_comprador'), table_name='boletos')
    op.drop_index(op.f('ix_boletos_id'), table_name='boletos')
    op.drop_index(op.f('ix_boletos_evento_id'), table_name='boletos')
    op.drop_table('boletos')
    op.drop_index(op.f('ix_eventos_nombre'), table_name='eventos')
    op.drop_index(op.f('ix_eventos_id'), table_name='eventos')
    op.drop_table('eventos')
