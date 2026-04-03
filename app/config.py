import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_default_123")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "Shruti@2005")
    DB_NAME = os.getenv("DB_NAME", "blood_bank")
    DEBUG = os.getenv("FLASK_ENV") == "development"
