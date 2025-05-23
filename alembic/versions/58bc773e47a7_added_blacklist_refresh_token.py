"""Added blacklist refresh token

Revision ID: 58bc773e47a7
Revises: b72f65217ca8
Create Date: 2025-03-26 13:50:21.751216

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '58bc773e47a7'
down_revision: Union[str, None] = 'b72f65217ca8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blacklist_refresh_tokens',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('revoked', sa.Boolean(), nullable=False),
    sa.Column('hashed_jti', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_user_hashed_jti', 'blacklist_refresh_tokens', ['user_id', 'hashed_jti'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('idx_user_hashed_jti', table_name='blacklist_refresh_tokens')
    op.drop_table('blacklist_refresh_tokens')
    # ### end Alembic commands ###
