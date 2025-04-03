from pydantic_settings import BaseSettings, SettingsConfigDict


class ApiConfig(BaseSettings):
    TITLE: str = "mango"
    HOST: str = "api"
    PORT: int = 8000

    VERSION: str = "0.1.0"

    DEBUG: bool = True
    LOG_LEVEL: str = "DEBUG"

    model_config = SettingsConfigDict(case_sensitive=True, env_prefix="AP_")
