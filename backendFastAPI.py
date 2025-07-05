from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class StepRequest(BaseModel):
    step: str

class ApplicationRequest(BaseModel):
    name: str
    email: str
    step: str

@app.post("/ai-suggestion")
async def ai_suggestion(req: StepRequest):
    suggestions = ["idle", "confused", "interested", "disinterested"]
    detected = random.choice(suggestions)
    return {"user_state": detected}

@app.post("/submit-application")
async def submit_application(data: ApplicationRequest):
    return {"status": "submitted", "data": data.dict()}
