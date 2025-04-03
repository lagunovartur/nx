from uuid import UUID

import pydantic as pd

import nx_api.infra.db.models as m
from nx_api.utils.pydantic.base_model import BaseModel
from nx_api.utils.pydantic.validators import Email, Phone, Password


class BaseUser(BaseModel):
    _model = m.User
    email: Email
    phone: Phone


class UserBase(BaseUser):
    id: UUID


class NewUser(BaseUser):
    id: UUID | None = None
    password: Password

    model_config = pd.ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "id": "05095dd9-57d2-4911-9b1d-638a60bdd653",
                    "email": "lagunovartur@inbox.ru",
                    "phone": "78524569685",
                    "password": "Qwerty!1",
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
