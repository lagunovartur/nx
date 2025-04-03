import re

import sqlalchemy.orm as orm
from sqlalchemy.orm import declared_attr


class Base(orm.DeclarativeBase):
    __mapper_args__ = {"eager_defaults": True}

    @declared_attr
    def __tablename__(cls):
        def camel_to_snake(name):
            return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()

        return camel_to_snake(cls.__name__)
