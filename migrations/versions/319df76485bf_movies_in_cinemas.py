"""movies in cinemas

Revision ID: 319df76485bf
Revises: ba73c3c882ab
Create Date: 2020-01-12 17:06:32.854443

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "319df76485bf"
down_revision = "ba73c3c882ab"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "items_in__provider",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("item_id", sa.Integer(), nullable=True),
        sa.Column("provider_id", sa.Integer(), nullable=True),
        sa.Column("valid_from", sa.DateTime(), nullable=True),
        sa.Column("valid_to", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["item_id"], ["item.id"],),
        sa.ForeignKeyConstraint(["provider_id"], ["provider.id"],),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_items_in__provider_valid_from"),
        "items_in__provider",
        ["valid_from"],
        unique=False,
    )
    op.create_index(
        op.f("ix_items_in__provider_valid_to"),
        "items_in__provider",
        ["valid_to"],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        op.f("ix_items_in__provider_valid_to"), table_name="items_in__provider"
    )
    op.drop_index(
        op.f("ix_items_in__provider_valid_from"), table_name="items_in__provider"
    )
    op.drop_table("items_in__provider")
    # ### end Alembic commands ###
