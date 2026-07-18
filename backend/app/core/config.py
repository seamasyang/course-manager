from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Course Manager API"
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/course_manager"
    debug: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()