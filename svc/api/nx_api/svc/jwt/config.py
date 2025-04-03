from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class JwtConfig(BaseSettings):

    SECRET_KEY: str
    ALG: str
    ACCESS_EXP: int = Field(..., description="Access token expiration time in minutes")
    REFRESH_EXP: int = Field(..., description="Refresh token expiration time in minutes")

    model_config = SettingsConfigDict(
        case_sensitive = True,
        env_prefix = 'JT_'
    )

