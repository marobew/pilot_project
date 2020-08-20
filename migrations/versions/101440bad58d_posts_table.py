"""posts table

Revision ID: 101440bad58d
Revises: 304359093894
Create Date: 2020-08-18 07:12:20.741039

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '101440bad58d'
down_revision = '304359093894'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('title', sa.String(length=20), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'title')
    # ### end Alembic commands ###
