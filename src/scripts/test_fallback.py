from app.services.text_verifier.fallback_check import google_search_fallback

if __name__ == "__main__":
    claim = "7.5 earthquake in Delhi today"
    result = google_search_fallback(claim)
    print("Fallback Search Results:")
    print(result)