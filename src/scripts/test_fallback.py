from app.services.text_verifier.fallback_check import fallback_search

if __name__ == "__main__":
    claim = "7.5 earthquake in Delhi today"
    result = fallback_search(claim)
    print("Fallback Search Results:")
    print(result)