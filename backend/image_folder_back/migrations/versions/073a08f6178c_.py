"""empty message

Revision ID: 073a08f6178c
Revises: a65c50b11600
Create Date: 2024-11-17 00:50:21.208675

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '073a08f6178c'
down_revision = 'a65c50b11600'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_unique_constraint('uq_users_user_username_email', 'users_user', ['username', 'email'])


def downgrade() -> None:
    op.drop_constraint('uq_users_user_username_email', 'users_user', type_='unique')
