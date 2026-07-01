from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY = "mysecretkey123"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

settings = Settings()