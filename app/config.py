import os


class Config:
    DB_URI = os.getenv("DB_URI", "postgresql+asyncpg://pythops:pythops@127.0.0.1:5432/pythops")


config = Config()
