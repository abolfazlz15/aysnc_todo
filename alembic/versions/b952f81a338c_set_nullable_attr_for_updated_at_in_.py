"""set nullable attr for updated_at in user and task

Revision ID: b952f81a338c
Revises: 34949d1e0127
Create Date: 2025-04-12 17:51:36.335726

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'b952f81a338c'
down_revision: Union[str, None] = '34949d1e0127'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('idx_user_hashed_jti', table_name='blacklist_refresh_tokens')
    op.create_index('idx_user_jti', 'blacklist_refresh_tokens', ['user_id', 'jti'], unique=False)
    op.alter_column('tasks', 'updated_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               nullable=True)
    op.alter_column('users', 'updated_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'updated_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               nullable=False)
    op.alter_column('tasks', 'updated_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               nullable=False)
    op.drop_index('idx_user_jti', table_name='blacklist_refresh_tokens')
    op.create_index('idx_user_hashed_jti', 'blacklist_refresh_tokens', ['user_id', 'jti'], unique=False)
    # ### end Alembic commands ###
