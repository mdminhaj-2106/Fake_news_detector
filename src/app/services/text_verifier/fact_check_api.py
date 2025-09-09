import requests
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from config.settings import settings
import os

BASE_URL = "https://factchecktools.googleapis.com/v1alpha1/claims:search"

<<<<<<< HEAD

def search_fact_check(claim: str, language: str = "en") -> dict:
=======
def get_authenticated_session():
    """
    Creates an authenticated session using service account credentials.
    """
    # Path to your service account JSON file
    credentials_path = settings.GCP_CREDENTIALS
    
    # Load credentials from the service account file
    credentials = service_account.Credentials.from_service_account_file(
        credentials_path,
        scopes=['https://www.googleapis.com/auth/factchecktools']
    )
    
    # Create an authenticated session
    session = requests.Session()
    
    # Get an access token
    credentials.refresh(Request())
    
    # Add the authorization header
    session.headers.update({
        'Authorization': f'Bearer {credentials.token}'
    })
    
    return session

def search_fact_check(claim: str, language: str = "en") -> list[dict]:
>>>>>>> e46e50d93b1e23b987ccab2ed1b5446856b7f8fd
    """
    Queries Google Fact Check API for a given claim using service account authentication.
    Returns structured evidence snippets.
    """
    try:
        # Get authenticated session
        session = get_authenticated_session()
        
        params = {
            "query": claim,
            "languageCode": language
        }
        
        resp = session.get(BASE_URL, params=params)
        resp.raise_for_status()
        data = resp.json()

        results = []
        for item in data.get("claims", []):
            review = item.get("claimReview", [{}])[0]
            results.append({
                "claim": item.get("text"),
                "rating": review.get("textualRating"),
                "publisher": review.get("publisher", {}).get("name"),
                "url": review.get("url")
            })
        return results
        
    except Exception as e:
        print(f"Error in fact check API: {e}")
        return []

def search_fact_check_with_api_key(claim: str, language: str = "en") -> list[dict]:
    """
    Fallback method using API key (keep as backup).
    """
    params = {
        "query": claim,
        "languageCode": language,
        "key": settings.FACT_CHECK_API_KEY,
    }
    resp = requests.get(BASE_URL, params=params)
    resp.raise_for_status()
    data = resp.json()

    results = []
    for item in data.get("claims", []):
        review = item.get("claimReview", [{}])[0]
        results.append(
            {
                "claim": item.get("text"),
                "rating": review.get("textualRating"),
                "publisher": review.get("publisher", {}).get("name"),
                "url": review.get("url"),
            }
        )

    # Return structured result with is_legit flag
    return {
        "is_legit": len(results) > 0
        and any(
            r.get("rating", "").lower() in ["true", "mostly true"] for r in results
        ),
        "evidence": results,
        "source": "fact_check_api",
    }
