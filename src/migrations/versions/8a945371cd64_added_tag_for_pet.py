"""added tag for pet

Revision ID: 8a945371cd64
Revises: 82127f59a4cd
Create Date: 2022-08-04 12:16:01.163888

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '8a945371cd64'
down_revision = '82127f59a4cd'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('tag',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=True),
                    sa.Column('pet_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['pet_id'], ['pet.id'],ondelete="CASCADE" ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.drop_constraint('pet_user_id_fkey', 'pet', type_='foreignkey')
    op.create_foreign_key(None, 'pet', 'users', ['user_id'], ['id'],ondelete="CASCADE")
    op.drop_constraint('store_pet_id_fkey', 'store', type_='foreignkey')
    op.create_foreign_key(None, 'store', 'pet', ['pet_id'], ['id'],ondelete="CASCADE")
    op.drop_index('ix_users_login', table_name='users')
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)


def downgrade():
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.create_index('ix_users_login', 'users', ['username'], unique=False)
    op.drop_table('tag')
