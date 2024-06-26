"""init

Revision ID: 7623ff0c141d
Revises: 
Create Date: 2024-03-23 18:21:50.288297

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7623ff0c141d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(sa.text("create schema users"))
    op.create_table('users',
    sa.Column('id', sa.Integer(), sa.Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=False),
    sa.Column('is_approved', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('password_hash', sa.CHAR(length=64), nullable=False),
    sa.Column('registered_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('users_pk')),
    sa.UniqueConstraint('email', name='users_unique_email'),
    schema='users'
    )
    op.create_table('notes',
    sa.Column('id', sa.Integer(), sa.Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('date_created', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.users.id'], name=op.f('notes_fk_user_id__users')),
    sa.PrimaryKeyConstraint('id', name=op.f('notes_pk'))
    )
    op.create_table('users_auth',
    sa.Column('id', sa.Integer(), sa.Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('device', sa.String(length=200), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('refresh_until', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('valid_until', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.users.id'], name=op.f('users_auth_fk_user_id__users')),
    sa.PrimaryKeyConstraint('id', name=op.f('users_auth_pk')),
    sa.UniqueConstraint('user_id', 'device', name='users_auth_unique_user_id_device'),
    schema='users'
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users_auth', schema='users')
    op.drop_table('notes')
    op.drop_table('users', schema='users')
    op.execute(sa.text("drop schema users"))
    # ### end Alembic commands ###
