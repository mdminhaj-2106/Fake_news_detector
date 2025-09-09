import vertexai
from vertexai.preview.generative_models import GenerativeModel



vertexai.init(
    project="fake-news-detector-471109", 
    location="us-central1"               
)

def gemini_flash_fake_news_check(text: str) -> str:
    # Use the Gemini 1.5 Flash model
    model = GenerativeModel("gemini-2.5-flash")
    prompt = (
        f"Analyze the following news text and determine if it is likely to be fake or real. "
        f"Explain your reasoning. Text: {text}"
    )
    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    result = gemini_flash_fake_news_check("This is a test news article.")
    print(result)