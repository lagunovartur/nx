"""init

Revision ID: 9236448c0c6b
Revises: 83e59b3900f9
Create Date: 2025-03-24 13:04:33.277055


"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '9236448c0c6b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")
    op.execute("CREATE EXTENSION IF NOT EXISTS btree_gist;")
    op.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")


def downgrade():
    op.execute("DROP EXTENSION IF EXISTS \"uuid-ossp\";")
    op.execute("DROP EXTENSION IF EXISTS btree_gist;")
    op.execute("DROP EXTENSION IF EXISTS pg_trgm;")
