import json
from .fact_check_api import search_fact_check
from .fallback_check import google_search_fallback
from .gemini_client import analyze_claim_with_gemini


def verify_news(text: str) -> dict:
    # 1. Fact Check (temporarily disabled for testing)
    try:
        fact_result = search_fact_check(text)
    except Exception as e:
        print(f"Fact Check API error: {e}")
        fact_result = {
            "is_legit": None,
            "evidence": ["Fact Check API unavailable"],
            "source": "fact_check_api_error",
        }

    # 2. Fallback if needed
    if not fact_result["is_legit"]:
        fallback_result = google_search_fallback(text)
    else:
        fallback_result = None

    # 3. Reasoning with Gemini
    gemini_result = analyze_claim_with_gemini(
        claim=text, fact_check=fact_result, fallback=fallback_result
    )

    # 4. Combine and return
    return {
        "fact_check": fact_result,
        "fallback": fallback_result,
        "gemini_reasoning": gemini_result,
        "final_verdict": gemini_result.get("verdict", "unknown"),
    }
