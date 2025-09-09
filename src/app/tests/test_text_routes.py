from google.cloud.aiplatform.gapic import PredictionServiceClient
import os
from dotenv import load_dotenv

PROJECT_ID =  os.getenv("PROJECT_ID")  
LOCATION = os.getenv("REGION")                


def test_vertex_ai_integration():
    client = PredictionServiceClient()
    endpoint = client.endpoint_path(
        project=PROJECT_ID, location=LOCATION
    )

    instance = {"content": "This is a test news article."}
    instances = [instance]
    parameters = {}

    response = client.predict(
        endpoint=endpoint, instances=instances, parameters=parameters
    )

    print("Vertex AI response:", response)


if __name__ == "__main__":
    test_vertex_ai_integration()
