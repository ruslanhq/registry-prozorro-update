"""Init

Revision ID: 1152fe57b014
Revises: 
Create Date: 2021-08-22 15:30:07.334558

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '1152fe57b014'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('prozorro_sale_auctions_history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('_id', sa.String(length=255), nullable=False),
    sa.Column('auction_id', sa.String(length=255), nullable=False),
    sa.Column('date_published', sa.String(length=255), nullable=False),
    sa.Column('date_modified', sa.String(length=255), nullable=False),
    sa.Column('object', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    schema='src'
    )
    op.create_index('prozorro_sale_auctions_history_id_date_modified_idx', 'prozorro_sale_auctions_history', ['_id', sa.text('date_modified DESC')], unique=False, schema='src')
    op.create_table('prozorro_sale_objects_history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('_id', sa.String(length=255), nullable=False),
    sa.Column('registry_object_id', sa.String(length=255), nullable=False),
    sa.Column('date_published', sa.String(length=255), nullable=False),
    sa.Column('date_modified', sa.String(length=255), nullable=False),
    sa.Column('object', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    schema='src'
    )
    op.create_index('prozorro_sale_objects_history_id_date_modified_idx', 'prozorro_sale_objects_history', ['_id', sa.text('date_modified DESC')], unique=False, schema='src')
    op.create_table('logs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('logger', sa.String(length=100), nullable=False),
    sa.Column('level', sa.String(length=100), nullable=False),
    sa.Column('trace', sa.String(length=4096), nullable=False),
    sa.Column('msg', sa.String(length=4096), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    schema='src'
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('prozorro_sale_objects_history_id_date_modified_idx', table_name='prozorro_sale_objects_history', schema='src')
    op.drop_table('prozorro_sale_objects_history', schema='src')
    op.drop_index('prozorro_sale_auctions_history_id_date_modified_idx', table_name='prozorro_sale_auctions_history', schema='src')
    op.drop_table('prozorro_sale_auctions_history', schema='src')
    op.drop_table('logs', schema='src')

    # ### end Alembic commands ###
