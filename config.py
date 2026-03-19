import os
import logging

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "devkey")
    DATABASE_URL = os.environ.get("DATABASE_URL")
    ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "12345")
    LOG_LEVEL = getattr(logging, os.environ.get("LOG_LEVEL", "DEBUG").upper(), logging.DEBUG)

class DevelopmentConfig(Config):
    LOG_LEVEL = logging.DEBUG

class ProductionConfig(Config):
    LOG_LEVEL = logging.WARNING