"""items are not unique

Revision ID: dc00e7d6038e
Revises: 319df76485bf
Create Date: 2020-01-16 21:21:00.798619

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "dc00e7d6038e"
down_revision = "319df76485bf"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("ix_item_name", table_name="item")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index("ix_item_name", "item", ["name"], unique=1)
    # ### end Alembic commands ###