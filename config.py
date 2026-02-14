import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "devkey")
    DATABASE_URL = os.environ.get("DATABASE_URL")
    ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "12345")