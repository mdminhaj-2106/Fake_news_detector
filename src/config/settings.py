import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    PROJECT_NAME = "Fake News Detector"
    API_KEY = os.getenv("API_KEY")
    JWT_SECERT_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM = "HS256"
    REDIS_URL = os.getenv("REDIS_URL")
    MODEL_PATH = "app/models/model.joblib"


settings = Settings()