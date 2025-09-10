import requests
from config.settings import settings

BASE_URL = "https://www.googleapis.com/customsearch/v1"

def google_search_fallback(claim: str, num_results: int = 5) -> dict:
    
    # Queries Google Custom Search API when Fact Check API has no results.
    # Returns a dict with the same structure as fact_check_api.py.
    

    API_KEY = settings.GOOGLE_CSE_API_KEY
    GOOGLE_CSE_ID = settings.GOOGLE_CSE_ID

    if not API_KEY or not GOOGLE_CSE_ID:
        return {
            "is_legit": None,
            "evidence": [],
            "source": "fallback_search_missing_credentials"
        }

    params = {
        "key": API_KEY,
        "cx": GOOGLE_CSE_ID,
        "q": claim,
        "num": num_results,
        "safe": "active",
    }

    try:
        resp = requests.get(BASE_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        results = []
        for item in data.get("items", []):
            results.append({
                "claim": claim,
                "rating": None,  # CSE doesn’t provide ratings
                "publisher": item.get("displayLink"),
                "url": item.get("link"),
            })

        return {
            "is_legit": len(results) > 0,
            "evidence": results[:num_results],
            "source": "fallback_search"
        }

    except Exception as e:
        print(f"[fallback_search] Error: {e}")
        return {
            "is_legit": None,
            "evidence": [],
            "source": "fallback_search_error"
        }


if __name__ == "__main__":
    claim = "7.5 earthquake in Delhi today"
    result = google_search_fallback(claim)
    print("Fallback Search Results:")
    print(result)