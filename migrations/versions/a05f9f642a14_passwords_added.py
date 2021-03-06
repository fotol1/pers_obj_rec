"""passwords added

Revision ID: a05f9f642a14
Revises: 26c43f047e87
Create Date: 2019-12-08 16:56:23.252237

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a05f9f642a14"
down_revision = "26c43f047e87"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "user", sa.Column("password_hash", sa.String(length=128), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("user", "password_hash")
    # ### end Alembic commands ###
