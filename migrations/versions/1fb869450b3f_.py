"""empty message

Revision ID: 1fb869450b3f
Revises: 213c24d21861
Create Date: 2013-12-03 12:59:27.569016

"""

# revision identifiers, used by Alembic.
revision = '1fb869450b3f'
down_revision = '213c24d21861'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('project', sa.Column('description', sa.String(length=2056), nullable=True))
    op.add_column('project', sa.Column('need', sa.String(length=2056), nullable=True))
    op.add_column('project', sa.Column('rewards', sa.String(length=512), nullable=True))
    op.add_column('project', sa.Column('status', sa.String(length=64), nullable=True))
    op.drop_column('project', u'info')
    op.drop_column('project', u'active')
    op.add_column('user', sa.Column('description', sa.String(length=2046), nullable=True))
    op.add_column('user', sa.Column('location', sa.String(length=64), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'location')
    op.drop_column('user', 'description')
    op.add_column('project', sa.Column(u'active', sa.BOOLEAN(), nullable=True))
    op.add_column('project', sa.Column(u'info', sa.VARCHAR(length=5012), nullable=True))
    op.drop_column('project', 'status')
    op.drop_column('project', 'rewards')
    op.drop_column('project', 'need')
    op.drop_column('project', 'description')
    ### end Alembic commands ###