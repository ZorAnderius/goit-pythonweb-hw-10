from dotenv import load_dotenv
import os

from pydantic import ConfigDict
from pydantic_settings import BaseSettings

load_dotenv('.env')

class Settings(BaseSettings):
    DB_URL: str = f"postgresql+asyncpg://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@postgres:5432/{os.getenv('POSTGRES_DB')}"
    JWT_SECRET_KEY: str = os.getenv('JWT_SECRET_KEY')
    JWT_ALGORITHM : str = os.getenv('JWT_ALGORITHM')
    JWT_EXPIRATION_TIME: str = os.getenv('JWT_TOKEN_EXPIRE_MINUTES')
    model_config = ConfigDict(
        extra="ignore", env_file=".env", env_file_encoding="utf-8", case_sensitive=True
    )

settings = Settings()