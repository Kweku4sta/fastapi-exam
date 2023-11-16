from pydantic_settings import BaseSettings


class Setting(BaseSettings):
    DATABASE_NAME: str = "fastapi"
    DATABASE_HOSTNAME: str = 'localhost'
    DATABASE_PORT: str = '5432'
    DATABASE_PASSWORD: str = 'database'
    DATABASE_USERNAME: str = 'postgres'
    SECRET_KEY: str = "FHHJGJHTGUERUGYUE7476578537567TFNGH8YUEYUHUWEU"
    ALGORITHM: str  = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = ".env"


settings = Setting()
