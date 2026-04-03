import os
from dotenv import load_dotenv, find_dotenv
# v4.6 Standard Config Node: Auto-Discovery
load_dotenv(find_dotenv())

class Config:
    # SaaS Security Node: Environment Variable Governance
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_surgical_mesh_123")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD") # No default to prevent leak
    DB_NAME = os.getenv("DB_NAME", "blood_bank")
    DEBUG = os.getenv("FLASK_ENV") == "development"
