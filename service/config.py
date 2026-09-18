"""
Flask application configuration, driven by environment variables so the
same image can run locally, in CI, or in Kubernetes.
"""
import os

DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///test.db")
SQLALCHEMY_DATABASE_URI = DATABASE_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.getenv("SECRET_KEY", "s3cr3t-key-shhhh")
LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO")
