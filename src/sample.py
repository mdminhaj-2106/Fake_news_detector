import os
from dotenv import load_dotenv
from google.oauth2 import service_account
import google.auth.transport.requests
import requests

# Load environment variables from .env
load_dotenv()

creds = service_account.Credentials.from_service_account_file(
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"],
    scopes=[
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/cloud-platform"
    ]
)

request = google.auth.transport.requests.Request()
creds.refresh(request)
token = creds.token

url = "https://factchecktools.googleapis.com/v1alpha1/claims:search"
params = {"query": "covid", "languageCode": "en"}
headers = {"Authorization": f"Bearer {token}"}

resp = requests.get(url, params=params, headers=headers)
print("Status:", resp.status_code)
print(resp.json())