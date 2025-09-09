import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    PROJECT_NAME = os.getenv("PROJECT_NAME", "Fake News Detector")
    PROJECT_ID = os.getenv("PROJECT_ID")
    FACT_CHECK_API_KEY = os.getenv("FACT_CHECK_API_KEY")
    REGION = os.getenv("REGION")
    GCP_CREDENTIALS = os.getenv(
        "GOOGLE_APPLICATION_CREDENTIALS", "google-credentials.json"
    )


settings = Settings()
