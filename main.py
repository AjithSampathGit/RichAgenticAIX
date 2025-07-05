from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class StepRequest(BaseModel):
    step: str

class HelpRequest(BaseModel):
    choice: str
    step: str = None

@app.post("/ai-suggestion")
async def ai_suggestion(req: StepRequest):
    # Randomly decide user state to simulate AI detection (with some bias per step)
    step = req.step
    weights = {
        "start": ["interested"]*5 + ["idle"]*1,
        "upload-id": ["confused"]*3 + ["interested"]*4 + ["idle"]*1,
        "terms": ["confused"]*3 + ["idle"]*2 + ["interested"]*3,
        "funding": ["idle"]*2 + ["interested"]*5 + ["confused"]*1,
        "thank-you": ["interested"]*7 + ["idle"]*1,
    }
    user_state = random.choice(weights.get(step, ["interested","idle","confused"]))
    
    # Suggestion message
    suggestions_map = {
        "idle": "Looks like you might be inactive. Need some help?",
        "confused": "You seem confused. How can I assist?",
        "disinterested": "Not sure about this step? I can help!",
        "interested": "You're doing great! Keep going!",
    }
    suggestion = suggestions_map.get(user_state, "Need help?")

    return {"user_state": user_state, "suggestion": suggestion}

@app.post("/ai-help")
async def ai_help(req: HelpRequest):
    choice = req.choice.lower()
    step = req.step or ""
    if choice == "live agent":
        # Provide chatbot with agent avatar
        return {
            "type": "chatbot",
            "agent_avatar": "https://randomuser.me/api/portraits/men/75.jpg",
            "agent_name": "Alex, Live Banker",
            "messages": ["Hello! How can I assist you with your Wells Fargo application today?"]
        }
    elif choice == "save for later":
        return {
            "type": "message",
            "content": "Your application has been saved. You can resume anytime."
        }
    elif choice == "explain product":
        return {
            "type": "message",
            "content": "Wells Fargo Checking offers no monthly fees with qualifying activities, access to over 13,000 ATMs, and mobile banking."
        }
    elif choice == "give feedback":
        # Survey questions
        return {
            "type": "survey",
            "questions": [
                "How easy was the application process?",
                "What would improve your experience?",
                "Would you recommend Wells Fargo to others?"
            ]
        }
    elif choice == "schedule appointment" or (choice == "live banker" and step=="terms"):
        # Calendar options for appointment setup
        slots = [
            "Monday 10:00 AM", "Tuesday 2:00 PM",
            "Wednesday 1:00 PM", "Thursday 3:30 PM",
            "Friday 11:00 AM"
        ]
        return {
            "type": "calendar",
            "slots": slots
        }
    else:
        return {
            "type": "message",
            "content": "Sorry, I didn't understand your choice. Please try again."
        }
