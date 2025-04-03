from functools import cached_property
from pydantic_settings import BaseSettings, SettingsConfigDict
from yarl import URL


class ApiConfig(BaseSettings):
    TITLE: str = "nx"

    HOST: str = "api"
    PORT: int = 8000

    DOMAIN: str = "localhost"
    DOMAIN_PORT: int = 8000

    VERSION: str = "1.0.0"
    OPENAPI_PATH: str = "api/swagger"

    DEBUG: bool = True
    INSTALL_DEV: bool = True
    LOG_LEVEL: str = "ERROR"

    @cached_property
    def URL(self) -> URL:
        return URL.build(scheme="https", host=self.DOMAIN, port=self.DOMAIN_PORT)

    @cached_property
    def API_URL(self) -> URL:
        return self.URL / "api"

    model_config = SettingsConfigDict(case_sensitive=True, env_prefix="AP_")
