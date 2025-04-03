from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisConfig(BaseSettings):

    HOST: str = 'redis'
    PORT: int = 6379
    DB: int = 0

    model_config = SettingsConfigDict(
        case_sensitive = True,
        env_prefix = 'RS_'
    )
