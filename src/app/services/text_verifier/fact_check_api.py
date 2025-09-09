import requests
from config.settings import settings

BASE_URL = "https://factchecktools.googleapis.com/v1alpha1/claims:search"

def search_fact_check(claim: str, language: str = "en") -> list[dict]:
    """
    Queries Google Fact Check API for a given claim.
    Returns structured evidence snippets.
    """
    params = {
        "query": claim,
        "languageCode": language,
        "key": settings.API_KEY
    }
    resp = requests.get(BASE_URL, params=params)
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
