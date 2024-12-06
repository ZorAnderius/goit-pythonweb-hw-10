from dotenv import load_dotenv
import os

load_dotenv('.env')

class Config:
    DB_URL = f"postgresql+asyncpg://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@postgres:5432/{os.getenv('POSTGRES_DB')}"
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')
    JWT_EXPIRATION_TIME = os.getenv('JWT_TOKEN_EXPIRE_MINUTES')

config = Config