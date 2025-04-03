from nx_api.utils.pydantic.base_model import BaseModel
from pydantic import Field


class Login(BaseModel):
    username: str = Field(examples=["simonov@example.com"])
    password: str = Field(examples=["Qwerty!1"])
