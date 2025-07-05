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

class HelpRequest(BaseModel):
    choice: str

@app.post("/ai-suggestion")
async def ai_suggestion(req: StepRequest):
    step = req.step
    user_states = ["idle", "confused", "interested", "disinterested"]
    detected = random.choices(user_states, weights=[0.3, 0.3, 0.3, 0.1])[0]

    suggestion_map = {
        "terms": "Would you like to talk to a banker about these terms?",
        "thank-you": "Would you like to give feedback about your experience?",
        "upload-id": "Having trouble uploading your ID?",
        "funding": "Need help funding your account?"
    }

    return {
        "user_state": detected,
        "suggestion": suggestion_map.get(step, "Need help completing this step?")
    }

@app.post("/ai-help")
async def ai_help(req: HelpRequest):
    choice = req.choice.lower()
    if "agent" in choice:
        return {
            "type": "chatbot",
            "agent_name": "Ashley (Banker Bot)",
            "agent_avatar": "https://www.wellsfargo.com/assets/images/icons/profile.png",
            "messages": ["Hi! I'm Ashley. I can assist you with any questions you have about the terms and conditions."]
        }
    elif "feedback" in choice:
        return {
            "type": "survey",
            "questions": [
                "What did you like about this experience?",
                "What could we do better?",
                "Would you recommend us to others?"
            ]
        }
    elif "calendar" in choice or "banker" in choice:
        return {
            "type": "calendar",
            "slots": [
                "Monday 10 AM", "Monday 2 PM",
                "Tuesday 11 AM", "Wednesday 1 PM"
            ]
        }
    else:
        return {
            "type": "info",
            "content": "Thanks! We're processing your request."
        }