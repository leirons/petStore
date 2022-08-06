import os


class Settings:
    DB = os.getenv(
        "DATABASE_URL",
    )
    TEST_DB = os.getenv(
        "TEST_DATABASE"
    )
    SECRET = os.getenv("SECRET_KEY")
    DSN = os.getenv("DSN")
    REDIS_HOST = os.getenv("REDIS_HOST")


settings = Settings()
