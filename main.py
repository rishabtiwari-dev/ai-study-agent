from fastapi import FastAPI
from pydantic import BaseModel
from agent import study_agent
from fastapi.middleware.cors import CORSMiddleware
import os

print("🔥 USING API KEY:", os.getenv("GOOGLE_API_KEY"))

# Create app ONCE
app = FastAPI()

# Enable CORS (for frontend connection)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class Request(BaseModel):
    text: str

# Health route
@app.get("/")
def home():
    return {"message": "AI Study Assistant is running 🚀"}

# Main route
@app.post("/study")
def study(req: Request):
    return study_agent(req.text)