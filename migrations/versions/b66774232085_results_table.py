"""results table

Revision ID: b66774232085
Revises: 2dd703deee99
Create Date: 2024-08-19 21:36:35.637650

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b66774232085'
down_revision = '2dd703deee99'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('result',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('hero_id', sa.Integer(), nullable=False),
    sa.Column('villain_id', sa.Integer(), nullable=False),
    sa.Column('result', sa.Enum('win', 'loss', name='resulttypes'), nullable=False),
    sa.ForeignKeyConstraint(['hero_id'], ['hero.id'], ),
    sa.ForeignKeyConstraint(['villain_id'], ['villain.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('result', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_result_hero_id'), ['hero_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_result_villain_id'), ['villain_id'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('result', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_result_villain_id'))
        batch_op.drop_index(batch_op.f('ix_result_hero_id'))

    op.drop_table('result')
    # ### end Alembic commands ###
