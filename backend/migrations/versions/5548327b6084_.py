"""empty message

Revision ID: 5548327b6084
Revises: 63cded931016
Create Date: 2024-01-05 18:29:52.151895

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5548327b6084'
down_revision = '63cded931016'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('locations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('itinerary',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('itinerary_name', sa.String(length=80), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('time_of_event', sa.DateTime(), nullable=True),
    sa.Column('event_name', sa.String(length=80), nullable=False),
    sa.Column('event_description', sa.String(length=80), nullable=False),
    sa.Column('event_location', sa.String(length=80), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('itinerary')
    op.drop_table('locations')
    # ### end Alembic commands ###
