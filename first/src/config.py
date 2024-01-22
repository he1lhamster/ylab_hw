from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Union, ClassVar


class Settings(BaseSettings):
    DB_HOST: Union[str | int]
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASS: str

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        extra="allow",
        env_file='.env'
    )

    @property
    def DB_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()
