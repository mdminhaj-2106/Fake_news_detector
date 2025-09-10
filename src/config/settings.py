import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    PROJECT_NAME = os.getenv("PROJECT_NAME", "Fake News Detector")
    PROJECT_ID = os.getenv("PROJECT_ID")
    API_KEY = os.getenv("API_KEY")  # Fixed: was FACT_CHECK_API_KEY
    REGION = os.getenv("REGION")
    GCP_CREDENTIALS = os.getenv(
        "GOOGLE_APPLICATION_CREDENTIALS", "fake-news-detector-471109-74393a5c71f6.json"
    )


settings = Settings()

# Debug logging
print("=== Environment Variables Debug ===")
print(f"PROJECT_ID: {settings.PROJECT_ID}")
print(f"REGION: {settings.REGION}")
print(f"API_KEY: {'SET' if settings.API_KEY else 'NOT SET'}")
print(f"GCP_CREDENTIALS: {settings.GCP_CREDENTIALS}")
print(f"Credentials file exists: {os.path.exists(settings.GCP_CREDENTIALS)}")
print("==================================")
