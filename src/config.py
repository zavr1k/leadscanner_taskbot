from pydantic import BaseSettings

MAX_USER_TASKS = 5


class Settings(BaseSettings):
    API_TOKEN: str

    WEBHOOK_HOST: str

    WEBAPP_HOST: str
    WEBAPP_PORT: str

    DATABASE_URL: str

    class Config:
        env_file = './.env'
        env_file_encoding = 'utf-8'


settings = Settings()
