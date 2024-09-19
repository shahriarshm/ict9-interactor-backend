from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:password@db:5432/mydatabase"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    WIDGET_SERVICE_URL: str = "http://192.168.1.15:9000/api/v1"
    WIDGET_SERVICE_TOKEN: str = "widget-service-token"
    DEFAULT_JS_URL: str = "http://192.168.1.12:3000/userTracker.js"
    OPENAI_API_KEY: str = "secret"
    OPENAI_API_URL: str = "https://api.openai.com/v1"

    class Config:
        env_file = ".env"


settings = Settings()
