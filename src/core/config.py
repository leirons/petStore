import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DB = os.getenv("DATABASE_URL",default="postgresql+asyncpg://test1:test3004@localhost/test_fastapi")
    TEST_DB = os.getenv("TEST_DATABASE",default="postgresql+asyncpg://test1:test3004@localhost/test")
    SECRET = os.getenv("SECRET_KEY", default="SECRET")
    DSN = os.getenv("DSN")


settings = Settings()
