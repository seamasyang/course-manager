from pydantic_settings import BaseSettings

import os
from dotenv import load_dotenv
load_dotenv()

print(f"env db===> {os.environ["DATABASE_URL"]}")

class Settings(BaseSettings):
    app_name: str = "Course Manager API"
    database_url: str = os.environ["DATABASE_URL"]
    debug: bool = True

settings = Settings()