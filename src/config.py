from pathlib import Path

from dotenv.variables import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODE:       str = ["LOCAL", "TEST", "DEV", "PROD"]
    DB_NAME:    str
    DB_PORT:    int
    DB_PASS:    str
    DB_HOST:    str
    DB_USER:    str
    SECRET_KEY: str
    ALGORITHM:  str

    model_config = SettingsConfigDict()

    class Config:
        env_file = Path(__file__).parent.parent / ".env"

    @property
    def DB_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()
