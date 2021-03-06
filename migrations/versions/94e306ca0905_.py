"""empty message

Revision ID: 94e306ca0905
Revises: None
Create Date: 2016-07-09 17:40:54.677548

"""

# revision identifiers, used by Alembic.
revision = '94e306ca0905'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blag',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('content', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tag',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tag_name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tags',
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.Column('bluhrg_post_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['bluhrg_post_id'], ['blag.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], )
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tags')
    op.drop_table('tag')
    op.drop_table('blag')
    ### end Alembic commands ###
