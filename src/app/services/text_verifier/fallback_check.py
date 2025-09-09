def google_search_fallback(claim: str) -> dict:
    """
    Fallback search when fact check API doesn't provide conclusive results.
    For now, returns a placeholder structure.
    """
    # TODO: Implement actual Google search or web scraping
    return {
        "is_legit": None,  # Unknown
        "evidence": [f"Fallback search for: {claim}"],
        "source": "fallback_search",
    }
