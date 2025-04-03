from typing import Literal
from uuid import UUID
import nx_api.infra.db.models as m
import pydantic as pd

from nx_api.utils.pydantic.base_model import BaseModel
from nx_api.utils.pydantic.validators import Email, Phone, Password


class BaseUser(BaseModel):
    _model = m.User
    email: Email
    phone: Phone


class UserBase(BaseUser):
    id: UUID


class NewUser(BaseUser):
    password: Password

    model_config = pd.ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "email": "lagunovartur@gmail.com",
                    "phone": "79124402323"
                },
            ]
        }
    )


class User(UserBase):
    pass


class EditUser(BaseUser):
    email: Email | None = None
    phone: Phone | None = None
    password: Password | None = None
