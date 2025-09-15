import os
import requests
from typing import List, Dict

API_KEY = os.getenv("API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")


def fallback_search(claim: str, num_results: int = 5) -> List[Dict]:
    """
    Queries Google Custom Search API when Fact Check API has no results.
    Returns a list of evidence snippets with title, snippet, source, and URL.
    """

    if not API_KEY or not GOOGLE_CSE_ID:
        raise ValueError("Missing Google Custom Search API credentials")

    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": API_KEY,
        "cx": GOOGLE_CSE_ID,
        "q": claim,
        "num": num_results,
        "safe": "active",
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"[fallback_search] Error fetching results: {e}")
        return []

    results = []
    for item in data.get("items", []):
        results.append({
            "title": item.get("title"),
            "snippet": item.get("snippet"),
            "source": item.get("displayLink"),
            "url": item.get("link"),
        })

    return results[:num_results]