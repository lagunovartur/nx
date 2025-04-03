from nx_api.utils.pydantic.base_model import BaseModel
from pydantic import Field
from nx_api.utils.pydantic.validators import Email

class Login(BaseModel):
    username: str = Field(examples=["lagunovartur@inbox.ru"])
    password: str = Field(examples=["Qwerty!1"])



class EmailReq(BaseModel):
    email: Email = Field(examples=["lagunovartur@inbox.ru"])
