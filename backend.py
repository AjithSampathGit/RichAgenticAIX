from flask import Flask, request, jsonify
import random

app = Flask(__name__)

@app.route("/ai-suggestion", methods=["POST"])
def ai_suggestion():
    user_step = request.json.get("step")
    suggestions = ["idle", "confused", "interested", "disinterested"]
    detected = random.choice(suggestions)
    return jsonify({"user_state": detected})

@app.route("/submit-application", methods=["POST"])
def submit_application():
    data = request.json
    return jsonify({"status": "submitted", "data": data})

if __name__ == "__main__":
    app.run(debug=True)