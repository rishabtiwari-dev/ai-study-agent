import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

def study_agent(user_text):
    try:
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"

        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": f"""
You are an AI Study Assistant.

From the given text:
1. Provide a short summary
2. Explain it simply
3. Generate exactly 3 quiz questions

Respond ONLY in valid JSON format:
{{
    "summary": "...",
    "simple_explanation": "...",
    "quiz_questions": ["...", "...", "..."]
}}

Text:
{user_text}
"""
                        }
                    ]
                }
            ]
        }

        response = requests.post(url, json=payload)
        data = response.json()

        text_output = data["candidates"][0]["content"]["parts"][0]["text"]

        return json.loads(text_output)

    except Exception as e:
        return {"error": str(e)}