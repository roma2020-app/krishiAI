import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from PIL import Image

# Load .env
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def analyze_leaf(image_path: str):

    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        return {
            "error": "GOOGLE_API_KEY not found"
        }

    client = genai.Client(api_key=api_key)

    image = Image.open(image_path)

    prompt = """
You are an expert agricultural scientist.

Analyze this crop leaf.

Return ONLY in this exact format.

Disease: <Disease Name>

Confidence: <0-100%>

Severity: Low / Medium / High

Symptoms:
- point1
- point2

Organic Treatment:
- point1
- point2

Chemical Treatment:
- point1
- point2

Prevention:
- point1
- point2

Should Farmer Visit RSK:
Yes or No
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            image,
            prompt
        ],
    )

    return response.text