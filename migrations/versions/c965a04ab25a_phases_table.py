"""phases table

Revision ID: c965a04ab25a
Revises: 8bb892b270a7
Create Date: 2024-07-28 09:57:41.063695

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c965a04ab25a'
down_revision = '8bb892b270a7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('phase',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('phasename', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('phase', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_phase_phasename'), ['phasename'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('phase', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_phase_phasename'))

    op.drop_table('phase')
    # ### end Alembic commands ###
