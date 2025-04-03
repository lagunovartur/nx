from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class JwtConfig(BaseSettings):
    SECRET_KEY: str = "some-secret-key"
    ALG: str = "HS256"
    ACCESS_EXP: int = Field(
        default=120, description="Access token expiration time in minutes"
    )
    REFRESH_EXP: int = Field(
        default=43200, description="Refresh token expiration time in minutes"
    )

    model_config = SettingsConfigDict(case_sensitive=True, env_prefix="JT_")
