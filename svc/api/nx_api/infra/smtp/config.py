from pydantic_settings import BaseSettings, SettingsConfigDict


class SmtpConfig(BaseSettings):

    HOST: str
    PORT: int
    EMAIL: str
    PASS: str

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_prefix='SM_'
    )
