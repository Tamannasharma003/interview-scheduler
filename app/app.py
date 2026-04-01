import os
import requests
from flask import Flask, request

from app.db import engine, SessionLocal
from model import Interview
from calendar_service import create_event  

from datetime import datetime
import json

app = Flask(__name__)

# ================================
# 🔹 DB SETUP
# ================================
Interview.metadata.create_all(bind=engine)

VERIFY_TOKEN = "tamanna_verify_token"

ACCESS_TOKEN = os.getenv("whatsapp_token")
PHONE_NUMBER_ID = os.getenv("phone_number_id")

MANAGER_PHONE = "918168100074"
CANDIDATE_PHONE = "919910105877"


# ================================
# 🔹 HOME
# ================================
@app.route("/")
def home():
    return "Server running ✅"


# ================================
# 🔹 SEND MESSAGE
# ================================
def send_whatsapp_message(to, message):
    print("🚀 Sending message...")

    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": message}
    }

    response = requests.post(url, headers=headers, json=data)
    print("📤 Status:", response.status_code)
    print("📤 Response:", response.text)


# ================================
# 🔹 WEBHOOK (FIXED)
# ================================
@app.route("/webhook", methods=["GET", "POST"])
def webhook():

    # 🔹 Verification
    if request.method == "GET":
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return "Verification failed", 403

    # 🔹 Incoming
    if request.method == "POST":
        print("📥 Webhook hit!")

        data = request.json
        print("📥 Incoming:", data)

        return "EVENT_RECEIVED", 200


# ================================
# 🚀 RUN
# ================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
