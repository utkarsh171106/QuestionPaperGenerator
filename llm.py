import requests
import os
from google import genai

def ollama_generate(prompt):
    url = "http://localhost:11434/api/generate"

    data = {
        "model": "qwen2.5:7b",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(url, json=data, timeout=10)

    if response.status_code != 200:
        raise Exception(f"Ollama HTTP error: {response.status_code}")

    return response.json()["response"]


def gemini_generate(prompt):
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        raise Exception("GEMINI_API_KEY is not set")

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


def generate_questions(prompt):

    try:
        print("Trying Ollama...")
        result = ollama_generate(prompt)

        print("Using Ollama")
        return result

    except Exception as e:
        print("Ollama unavailable:", e)
        print("Switching to Gemini...")

        try:
            result = gemini_generate(prompt)

            print("Using Gemini")
            return result

        except Exception as e:
            print("Gemini unavailable:", e)
            return "Both Ollama and Gemini are unavailable."