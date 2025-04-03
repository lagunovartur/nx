from pydantic_settings import BaseSettings, SettingsConfigDict


class UrlTokenConfig(BaseSettings):

    SECRET_KEY: str
    SALT: str

    model_config = SettingsConfigDict(
        case_sensitive = True,
        env_prefix = 'ID_'
    )

