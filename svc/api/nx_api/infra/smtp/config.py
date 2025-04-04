from pydantic_settings import BaseSettings, SettingsConfigDict


class SmtpConfig(BaseSettings):
    HOST: str = 'smtp.mail.ru'
    PORT: int = 465
    EMAIL: str = 'somemail@mail.ru'
    PASS: str = 'some_password'

    model_config = SettingsConfigDict(case_sensitive=True, env_prefix="SM_")
