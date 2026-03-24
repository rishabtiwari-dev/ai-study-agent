from fastapi import FastAPI
from pydantic import BaseModel
from agent import study_agent

app = FastAPI()

class Request(BaseModel):
    text: str

@app.get("/")
def home():
    return {"message": "AI Study Assistant is running 🚀"}

@app.post("/study")
def study(req: Request):
    return study_agent(req.text)