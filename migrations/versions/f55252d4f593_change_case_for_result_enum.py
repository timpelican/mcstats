"""change case for result enum

Revision ID: f55252d4f593
Revises: b66774232085
Create Date: 2024-08-26 20:43:17.930679

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f55252d4f593'
down_revision = 'b66774232085'
branch_labels = None
depends_on = None


def upgrade():
    # Put all values in enum
    op.execute("ALTER TABLE result MODIFY result enum('WIN','LOSS','win','loss')")
    # Update values to upper-case
    op.execute("UPDATE result SET result='WIN' where result='win'")
    op.execute("UPDATE result SET result='LOSS' where result='loss'")
    # Remove lower-case values
    op.execute("ALTER TABLE result MODIFY result enum('WIN','LOSS')")

def downgrade():
    op.execute("ALTER TABLE result MODIFY result enum('WIN','LOSS','win','loss')")
    # Update values to lower-case
    op.execute("UPDATE result SET result='win' where result='WIN'")
    op.execute("UPDATE result SET result='loss' where result='LOSS'")
    # Remove upper-case values
    op.execute("ALTER TABLE result MODIFY result enum('win','loss')")

