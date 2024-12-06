from dotenv import load_dotenv
import os

load_dotenv('.env')

class Config:
    DB_URL = f"postgresql+asyncpg://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@postgres:5432/{os.getenv('POSTGRES_DB')}"

config = Config