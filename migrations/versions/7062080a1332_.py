"""empty message

Revision ID: 7062080a1332
Revises: 318e02e4773c
Create Date: 2025-03-16 21:29:31.443153

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7062080a1332'
down_revision = '318e02e4773c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_profiles', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password', sa.String(length=128), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_profiles', schema=None) as batch_op:
        batch_op.drop_column('password')

    # ### end Alembic commands ###
