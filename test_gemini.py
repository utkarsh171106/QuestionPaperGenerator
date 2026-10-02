import os
from google import genai

key = os.getenv("GEMINI_API_KEY")

if not key:
    print("GEMINI_API_KEY is not set")
    exit()

client = genai.Client(api_key=key)

response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="Generate one simple question about Object Oriented Programming."
)

print(response.text)