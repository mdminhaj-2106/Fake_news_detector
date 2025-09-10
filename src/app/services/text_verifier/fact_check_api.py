import requests
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from config.settings import settings
import os

# Try the v1 endpoint instead of v1alpha1
BASE_URL = "https://factchecktools.googleapis.com/v1/claims:search"


def get_authenticated_session():
    # Creates an authenticated session using service account credentials.

    # Path to your service account JSON file
    credentials_path = settings.GCP_CREDENTIALS

    # Load credentials from the service account file
    credentials = service_account.Credentials.from_service_account_file(
        credentials_path, scopes=["https://www.googleapis.com/auth/factchecktools"]
    )

    # Create an authenticated session
    session = requests.Session()

    # Get an access token
    credentials.refresh(Request())

    # Add the authorization header
    session.headers.update({"Authorization": f"Bearer {credentials.token}"})

    return session


def search_fact_check(claim: str, language: str = "en") -> dict:
    """
    Queries Google Fact Check API for a given claim using service account authentication.
    Falls back to API key method if service account fails.
    Returns structured evidence snippets with shape:
    { is_legit: bool | None, evidence: list[dict], source: str }
    """
    try:
        # Try service account authentication first
        session = get_authenticated_session()

        params = {"query": claim, "languageCode": language}

        resp = session.get(BASE_URL, params=params)
        resp.raise_for_status()
        data = resp.json()

        evidence = []
        for item in data.get("claims", []):
            review = item.get("claimReview", [{}])[0]
            evidence.append(
                {
                    "claim": item.get("text"),
                    "rating": review.get("textualRating"),
                    "publisher": review.get("publisher", {}).get("name"),
                    "url": review.get("url"),
                }
            )

        return {
            "is_legit": len(evidence) > 0,  # True if we found evidence
            "evidence": evidence,
            "source": "fact_check_api",
        }

    except Exception as e:
        print(f"Service account authentication failed: {e}")
        print("Falling back to API key method...")

        # Fallback to API key method
        try:
            if not settings.API_KEY:
                raise ValueError("No API key available for fallback")

            params = {"query": claim, "languageCode": language, "key": settings.API_KEY}
            resp = requests.get(BASE_URL, params=params)
            resp.raise_for_status()
            data = resp.json()

            evidence = []
            for item in data.get("claims", []):
                # Handle claimReview - it can be a list or a single dict
                claim_reviews = item.get("claimReview", [])
                if isinstance(claim_reviews, list) and len(claim_reviews) > 0:
                    review = claim_reviews[0]
                elif isinstance(claim_reviews, dict):
                    review = claim_reviews
                else:
                    review = {}

                evidence.append(
                    {
                        "claim": item.get("text"),
                        "rating": review.get("textualRating"),
                        "publisher": review.get("publisher", {}).get("name"),
                        "url": review.get("url"),
                    }
                )

            return {
                "is_legit": len(evidence) > 0,
                "evidence": evidence,
                "source": "fact_check_api_key",
            }

        except Exception as fallback_error:
            print(f"API key fallback also failed: {fallback_error}")
            return {
                "is_legit": None,
                "evidence": ["Fact Check API unavailable"],
                "source": "fact_check_api_error",
            }


def search_fact_check_with_api_key(claim: str, language: str = "en") -> dict:
    """
    Fallback method using API key (keep as backup).
    Returns a dict with keys: is_legit, evidence, source.
    """
    try:
        params = {
            "query": claim,
            "languageCode": language,
            "key": settings.API_KEY,
        }
        resp = requests.get(BASE_URL, params=params)
        resp.raise_for_status()
        data = resp.json()

        results = []
        for item in data.get("claims", []):
            # Handle claimReview - it can be a list or a single dict
            claim_reviews = item.get("claimReview", [])
            if isinstance(claim_reviews, list) and len(claim_reviews) > 0:
                review = claim_reviews[0]
            elif isinstance(claim_reviews, dict):
                review = claim_reviews
            else:
                review = {}

            results.append(
                {
                    "claim": item.get("text"),
                    "rating": review.get("textualRating"),
                    "publisher": review.get("publisher", {}).get("name"),
                    "url": review.get("url"),
                }
            )

        return {
            "is_legit": len(results) > 0,
            "evidence": results,
            "source": "fact_check_api_key",
        }
    except Exception as e:
        print(f"Error in fact check API key method: {e}")
        return {
            "is_legit": None,
            "evidence": [],
            "source": "fact_check_api_key_error",
        }
