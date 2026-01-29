import os

SQLALCHEMY_DATABASE_URI = os.getenv(
    "SQLALCHEMY_DATABASE_URI", "sqlite:///expenses.sqlite3"
)

SWAGGER_UI_URL = "/docs"
SWAGGER_API_URL = "/spec"

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
