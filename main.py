from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
from datetime import datetime, timedelta

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

class ChoiceRequest(BaseModel):
    choice: str

@app.post("/ai-suggestion")
def ai_suggestion(req: StepRequest):
    # Randomly simulate AI detecting trouble based on step
    step = req.step
    state = random.choices(
        population=["interested", "idle", "confused", "disinterested"],
        weights=[0.6, 0.1, 0.2, 0.1],
        k=1
    )[0]

    suggestion = ""
    if state == "confused":
        suggestion = f"Would you like help with the '{step}' step? You can connect with a bot or see FAQs."
    elif state == "disinterested":
        suggestion = "Looks like you’re not very engaged. Want to save this for later or speak to a banker?"

    return {"user_state": state, "suggestion": suggestion}


@app.post("/ai-help")
def ai_help(req: ChoiceRequest):
    choice = req.choice.lower()

    if "live" in choice:
        return {
            "type": "chatbot",
            "agent_name": "Alex the Banker",
            "agent_avatar": "https://randomuser.me/api/portraits/men/32.jpg",
            "messages": ["Hi, I'm Alex. How can I help you today?"]
        }

    elif "survey" in choice:
        return {
            "type": "survey",
            "questions": [
                "What was unclear during the application?",
                "How likely are you to recommend this experience?",
                "What could be improved?"
            ]
        }

    elif "appointment" in choice:
        today = datetime.now()
        slots = [(today + timedelta(days=i)).strftime("%Y-%m-%d 10:00 AM") for i in range(1, 6)]
        return {
            "type": "calendar",
            "slots": slots
        }

    elif "explain" in choice:
        return {
            "type": "text",
            "content": "Wells Fargo Checking gives you zero-liability protection, mobile check deposit, and access to over 12,000 ATMs nationwide."
        }

    else:
        return {"type": "text", "content": "No help content available."}
