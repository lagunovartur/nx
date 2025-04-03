import sqlalchemy.orm as orm
from sqlalchemy.orm import declared_attr


class Base(orm.DeclarativeBase):
    __mapper_args__ = {"eager_defaults": True}

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
