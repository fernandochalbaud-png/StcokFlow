"""agrega tabla empresa_logs

Revision ID: 18e3b755d1b5
Revises: 
Create Date: 2026-03-19 19:55:37.547454

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '18e3b755d1b5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('empresa_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('empresa_id', sa.Integer(), nullable=False),
        sa.Column('evento', sa.String(length=50), nullable=False),
        sa.Column('fecha', sa.DateTime(), nullable=True),
        sa.Column('notas', sa.String(length=200), nullable=True),
        sa.ForeignKeyConstraint(['empresa_id'], ['empresas.id'], name='fk_empresalog_empresa'),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('empresa_logs')
