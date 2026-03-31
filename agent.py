import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

def clean_text(text):
    text = text.strip()
    text = text.replace("```json", "").replace("```", "")
    return text.strip()

def study_agent(user_text):
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

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
            ],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 512
            }
        }

        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(url, headers=headers, json=payload)

        # 🔥 DEBUG (keep this for now)
        print("STATUS:", response.status_code)
        print("RAW RESPONSE:", response.text)

        data = response.json()

        # ❌ If API error
        if response.status_code != 200:
            return {
                "error": "API request failed",
                "details": data
            }

        # ❌ If no candidates
        if "candidates" not in data or len(data["candidates"]) == 0:
            return {
                "error": "No candidates returned",
                "details": data
            }

        parts = data["candidates"][0]["content"].get("parts", [])

        if not parts:
            return {
                "error": "Empty response from model",
                "details": data
            }

        text_output = parts[0].get("text", "")

        if not text_output:
            return {
                "error": "No text in response",
                "details": data
            }

        cleaned = clean_text(text_output)

        # ✅ Try parsing JSON
        try:
            return json.loads(cleaned)
        except:
            return {
                "error": "Invalid JSON from model",
                "raw_output": cleaned
            }

    except Exception as e:
        return {"error": str(e)}