from vertexai.preview.generative_models import GenerativeModel

gemini = GenerativeModel("gemini-2.5-pro")

def analyze_claim_with_gemini(claim: str, evidence: list[str]) -> dict:

    # Claim and evidence from FactCheckAPI or FallbackCheck.
    # Sends the claim and evidence snippets to Gemini Flash.
    # Returns stance, confidence score, explanation, and tip.
    
    prompt = f"""
        Claim: "{claim}"
        Evidence: {evidence}

        Instructions:
        1. Decide if the claim is Supported, Refuted, or Uncertain.
        2. Give confidence score between 0 and 1.
        3. Provide short explanation citing sources.
        4. Provide a 1-line educational tip.

        Return JSON with keys: label, score, explanation, tip.
    """
    response = gemini.generate_content(prompt)
    return response.text
