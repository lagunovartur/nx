from pydantic_settings import BaseSettings, SettingsConfigDict


class DbConfig(BaseSettings):
    USER: str = 'postgres'
    PASS: str = 'postgres'
    HOST: str = 'localhost'
    PORT: int = 5432
    NAME: str = 'postgres'
    ECHO: bool = False
    POOL_SIZE: int = 64
    MAX_OVERFLOW: int = 10

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
