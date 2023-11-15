import os

from dotenv import load_dotenv
from pydantic import BaseSettings

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
    MONGO_CONTAINER_NAME: str = os.getenv("CONTAINER_NAME")

    # Minio connection
    MINIO_HOST: str = os.getenv("MINIO_HOST")
    MINIO_PORT: str = os.getenv("MINIO_PORT")
    MINIO_ACCESS_KEY: str = os.getenv("MINIO_ACCESS_KEY")
    MINIO_SECRET_KEY: str = os.getenv("MINIO_SECRET_KEY")
    MINIO_BUCKET_NAME: str = os.getenv("MINIO_BUCKET_NAME")

    # Uvicorn
    UVICORN_HOST: str = os.getenv("UVICORN_HOST")
    UVICORN_PORT: int = int(os.getenv("UVICORN_PORT"))

    # Auth
    SECRET_KEY: str = os.getenv("SECRET_KEY")

    MONGO_CLIENT: str = os.getenv("MONGO_CLIENT") or "server"


settings = Settings()
