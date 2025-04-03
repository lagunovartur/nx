from pydantic_settings import BaseSettings, SettingsConfigDict


class DbConfig(BaseSettings):
    USER: str
    PASS: str
    HOST: str
    PORT: int
    NAME: str
    ECHO: bool
    POOL_SIZE: int
    MAX_OVERFLOW: int

    @property
    def ASYNC_URL(self):
        return (
            f"postgresql+asyncpg://{self.USER}:"
            f"{self.PASS}@{self.HOST}:{self.PORT}/{self.NAME}"
        )

    @property
    def SYNC_URL(self):
        return (
            f"postgresql://{self.USER}:{self.PASS}@{self.HOST}:{self.PORT}/{self.NAME}"
        )

    model_config = SettingsConfigDict(case_sensitive=True, env_prefix="DB_")
