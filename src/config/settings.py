import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    PROJECT_NAME = os.getenv("PROJECT_NAME", "Fake News Detector")
    PROJECT_ID = os.getenv("PROJECT_ID")
    API_KEY = os.getenv("API_KEY")
    REGION = os.getenv("REGION")
    GCP_CREDENTIALS = os.getenv(
        "GOOGLE_APPLICATION_CREDENTIALS", "service_account.json"
    )
    GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")


settings = Settings()
