from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
import os
import requests

# Load environment variables
load_dotenv()
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ AI Wellness Chatbot is running!"

@app.route("/sms", methods=["POST"])
def sms_reply():
    incoming_msg = request.form.get("Body", "")
    user_number = request.form.get("From", "")

    # Claude API headers
    headers = {
        "x-api-key": CLAUDE_API_KEY,
        "content-type": "application/json",
        "anthropic-version": "2023-06-01"
    }

    # Claude API payload
    payload = {
        "model": "claude-3-haiku-20240307",
        "max_tokens": 200,
        "messages": [
            {
                "role": "user",
                "content": f"You are a compassionate wellness assistant. Help the user who says: '{incoming_msg}'"
            }
        ]
    }

    try:
        response = requests.post("https://api.anthropic.com/v1/messages", headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        claude_reply = data["content"][0]["text"]

        # Add welcome + disclaimer
        final_reply = (
            "🩺 Welcome to Info Health AI\n"
            "⚠️ Disclaimer: This tool provides general wellness information and is not a substitute for professional medical advice.\n\n"
            f"{claude_reply}"
        )
    except Exception as e:
        final_reply = "Sorry, there was a problem responding."

    twilio_response = MessagingResponse()
    twilio_response.message(final_reply)
    return str(twilio_response)

if __name__ == "__main__":
    app.run(debug=True)
