from pydantic import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    # Settings
    APP_NAME: str = os.getenv("APP_NAME")
    DEBUG_MODE: bool = os.getenv("DEBUG_MODE")

    # RabbitMQ
    MONGO_HOST: str = os.getenv("MONGO_HOST")
    MONGO_PORT: int = int(os.getenv("MONGO_PORT"))
    MONGO_USER: str = os.getenv("MONGO_USER")
    MONGO_PASS: str = os.getenv("MONGO_PASS")
    MONGO_CONTAINERNAME: str = os.getenv("CONTAINERNAME")

    # Uvicorn
    UVICORN_HOST: str = os.getenv("UVICORN_HOST")
    UVICORN_PORT: int = int(os.getenv("UVICORN_PORT"))

    # Auth
    SECRET_KEY: str = os.getenv("SECRET_KEY")

settings = Settings()
