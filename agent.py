import os
import json
from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def clean_json(text):
    text = text.strip()

    if text.startswith("```json"):
        text = text[7:]
    if text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]

    return text.strip()

def study_agent(user_text):
    try:
        prompt = f"""
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

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        cleaned = clean_json(response.text)

        try:
            data = json.loads(cleaned)
        except:
            return {
                "error": "Invalid JSON from model",
                "raw_output": cleaned
            }

        return data

    except Exception as e:
        return {"error": str(e)}