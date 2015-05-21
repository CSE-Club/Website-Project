"""Added content.render_template

Revision ID: 391308071ed
Revises: 10e1388006e
Create Date: 2015-05-20 12:20:13.774339

"""

# revision identifiers, used by Alembic.
revision = '391308071ed'
down_revision = '10e1388006e'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('content', sa.Column('render_template', sa.Text(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('content', 'render_template')
    ### end Alembic commands ###