"""tabla_user_agregado_campo_phone

Revision ID: a65a8ce094da
Revises: 
Create Date: 2025-01-20 13:42:32.737328

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a65a8ce094da'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('user', sa.Column('phone', sa.String(50), nullable=True))


def downgrade() -> None:
    op.drop_column('user', 'phone')
