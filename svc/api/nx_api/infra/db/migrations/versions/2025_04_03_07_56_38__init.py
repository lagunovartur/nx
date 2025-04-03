"""init

Revision ID: 93a8e770c719
Revises: 9236448c0c6b
Create Date: 2025-04-03 07:56:38.609585

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "93a8e770c719"
down_revision = "9236448c0c6b"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user",
        sa.Column("email", sa.String(length=50), nullable=True),
        sa.Column("phone", sa.String(length=11), nullable=True),
        sa.Column("password", sa.String(length=60), nullable=True),
        sa.Column(
            "email_verified",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
        sa.Column(
            "id",
            sa.UUID(),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("phone"),
    )
    op.create_table(
        "auth_sess",
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("ip_addr", sa.String(length=45), nullable=False),
        sa.Column(
            "status",
            sa.Enum(
                "ACTIVE", "COMPLETED", "HACKED", name="sessstatus", native_enum=False
            ),
            nullable=False,
        ),
        sa.Column(
            "id",
            sa.UUID(),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "refresh_token",
        sa.Column("session_id", sa.UUID(), nullable=False),
        sa.Column("parent_id", sa.UUID(), nullable=True),
        sa.Column("expires_at", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column(
            "id",
            sa.UUID(),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["parent_id"], ["refresh_token.id"], ondelete="SET NULL"
        ),
        sa.ForeignKeyConstraint(["session_id"], ["auth_sess.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("refresh_token")
    op.drop_table("auth_sess")
    op.drop_table("user")
    # ### end Alembic commands ###
