"""post update

Revision ID: 115e93588e6d
Revises: a44ae8116168
Create Date: 2020-08-18 23:21:19.379654

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '115e93588e6d'
down_revision = 'a44ae8116168'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('content', sa.String(length=280), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'content')
    # ### end Alembic commands ###