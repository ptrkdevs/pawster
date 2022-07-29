"""empty message

Revision ID: 9f8a196f6cf3
Revises: 66bc7b420b43
Create Date: 2022-07-29 20:21:05.594671

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f8a196f6cf3'
down_revision = '66bc7b420b43'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('profile_image', sa.String(length=64), nullable=True),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=65), nullable=False),
    sa.Column('address', sa.String(length=200), nullable=True),
    sa.Column('contact_number', sa.String(length=11), nullable=True),
    sa.Column('password', sa.String(length=250), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.drop_table('user')
    op.drop_constraint('pet_owner_id_fkey', 'pet', type_='foreignkey')
    op.create_foreign_key(None, 'pet', 'users', ['owner_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'pet', type_='foreignkey')
    op.create_foreign_key('pet_owner_id_fkey', 'pet', 'user', ['owner_id'], ['id'])
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('profile_image', sa.VARCHAR(length=64), autoincrement=False, nullable=True),
    sa.Column('name', sa.VARCHAR(length=64), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(length=65), autoincrement=False, nullable=False),
    sa.Column('address', sa.VARCHAR(length=200), autoincrement=False, nullable=True),
    sa.Column('contact_number', sa.VARCHAR(length=11), autoincrement=False, nullable=True),
    sa.Column('password', sa.VARCHAR(length=250), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='user_pkey'),
    sa.UniqueConstraint('email', name='user_email_key')
    )
    op.drop_table('users')
    # ### end Alembic commands ###
