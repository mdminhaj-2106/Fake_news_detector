import os
import vertexai
from vertexai.generative_models import GenerativeModel
from dotenv import load_dotenv

load_dotenv()

# Load environment variables
PROJECT_ID = os.getenv("PROJECT_ID")
REGION = os.getenv("REGION")

if not all([PROJECT_ID, REGION]):
    print("Error: Please make sure PROJECT_ID and REGION are set in your .env file.")
else:
    try:
        # Initialize Vertex AI
        vertexai.init(project=PROJECT_ID, location=REGION)

        # Load the Gemini Flash model
        model = GenerativeModel("gemini-2.5-flash")

        # Send a simple prompt
        prompt = "Hello, what is your name?"
        print(f"Sending prompt: '{prompt}'")

        # Get the response
        response = model.generate_content(prompt)

        # Print the response text
        print("\nModel Response:")
        print(response.text)
        print("\n Gemini 2.5 Flash test successful!")

    except Exception as e:
        print(f"\n An error occurred during the test:")
        print(e)
        print("\nPlease check your API keys, project ID, region, and service account authentication.")