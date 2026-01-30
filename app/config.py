import os

SWAGGER_UI_URL = "/docs"
SWAGGER_API_URL = "/spec"


class Config:
    TESTING = False

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "SQLALCHEMY_DATABASE_URI", "sqlite:///expenses.sqlite3"
    )

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")


class TestingConfig(Config):
    TESTING = True

    SQLALCHEMY_DATABASE_URI = "sqlite:///test.sqlite3"
