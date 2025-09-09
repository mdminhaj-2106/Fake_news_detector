import vertexai
from vertexai.preview.generative_models import GenerativeModel
from config.settings import settings

vertexai.init(project=settings.PROJECT_ID, location=settings.REGION)

gemini = GenerativeModel("gemini-2.5-pro")


def analyze_claim_with_gemini(
    claim: str, fact_check: dict, fallback: dict = None
) -> dict:
    # Claim and evidence from FactCheckAPI or FallbackCheck.
    # Sends the claim and evidence snippets to Gemini Flash.
    # Returns stance, confidence score, explanation, and tip.

    # Combine evidence from fact check and fallback
    evidence_text = f"Fact Check: {fact_check.get('evidence', [])}"
    if fallback:
        evidence_text += f"\nFallback: {fallback.get('evidence', [])}"

    prompt = f"""
        Claim: "{claim}"
        Evidence: {evidence_text}

        Instructions:
        1. Decide if the claim is Supported, Refuted, or Uncertain.
        2. Give confidence score between 0 and 1.
        3. Provide short explanation citing sources.
        4. Provide a 1-line educational tip.

        Return JSON with keys: label, score, explanation, tip, verdict.
    """
    response = gemini.generate_content(prompt)

    # Parse JSON response and return as dict
    try:
        import json

        return json.loads(response.text)
    except Exception as e:
        return {
            "label": "Uncertain",
            "score": 0.5,
            "explanation": "Unable to parse Gemini response",
            "tip": "Please try again",
            "verdict": "unknown",
        }
