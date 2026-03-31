# test_key.py - run this locally
import requests
import os
from dotenv import load_dotenv
load_dotenv()

key = os.getenv("GEMINI_API_KEY")
print("Key found:", key[:10] if key else "NONE")

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"
payload = {"contents": [{"parts": [{"text": "Say hello"}]}]}
r = requests.post(url, json=payload)
print("Status:", r.status_code)
print("Response:", r.text[:300])