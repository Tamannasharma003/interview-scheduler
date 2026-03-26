import os
import requests
from flask import Flask, request

from database import engine, SessionLocal
from model import Interview
from calendar_service import create_event
from datetime import datetime

# ✅ Create tables
Interview.metadata.create_all(bind=engine)

app = Flask(__name__)

VERIFY_TOKEN = "tamanna_verify_token"

ACCESS_TOKEN = os.getenv("whatsapp_token")
PHONE_NUMBER_ID = os.getenv("phone_number_id")

# ✅ Phone numbers (NO + sign)
MANAGER_PHONE = "918168100074"
CANDIDATE_PHONE = "919910105877"


# 🔹 Send WhatsApp Message
def send_whatsapp_message(to, message):
    if not ACCESS_TOKEN or not PHONE_NUMBER_ID:
        print("❌ Missing ENV variables")
        return

    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {
            "body": message
        }
    }

    response = requests.post(url, headers=headers, json=data)

    print("📤 Sent to:", to)
    print("💬 Message:", message)
    print("STATUS:", response.status_code)
    print("RESPONSE:", response.text)


# 🔹 Startup message
def send_startup_message():
    print("🚀 Sending startup message")

    send_whatsapp_message(
        MANAGER_PHONE,
        "Hi 👋 What are your free interview slots today?"
    )


# 🔹 Run once
@app.before_request
def run_once():
    if not hasattr(app, "startup_done"):
        send_startup_message()
        app.startup_done = True


# ✅ Home
@app.route("/")
def home():
    return "Server running ✅"


# ✅ Webhook
@app.route("/webhook", methods=["GET", "POST"])
def webhook():

    # 🔹 Verification
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode == "subscribe" and token == VERIFY_TOKEN:
            return str(challenge), 200
        else:
            return "Verification failed", 403

    # 🔹 Incoming messages
    if request.method == "POST":
        data = request.json
        print("📥 Incoming:", data)

        try:
            if "entry" in data:
                for entry in data["entry"]:
                    for change in entry.get("changes", []):
                        value = change.get("value", {})

                        if "messages" in value:
                            msg = value["messages"][0]

                            sender = msg.get("from", "")
                            sender = sender.replace(" ", "").replace("+", "").strip()

                            if msg.get("type") == "text":
                                message = msg.get("text", {}).get("body", "").lower().strip()
                            else:
                                message = ""

                            print("👤 Sender:", sender)
                            print("💬 Message:", message)

                            # =========================
                            # ✅ MANAGER FLOW
                            # =========================
                            if sender.endswith(MANAGER_PHONE[-10:]):
                                print("📌 Manager detected")

                                db = SessionLocal()

                                new_interview = Interview(
                                    manager_id=MANAGER_PHONE,
                                    candidate_id=CANDIDATE_PHONE,
                                    slots=message,
                                    status="pending"
                                )

                                db.add(new_interview)
                                db.commit()
                                db.close()

                                send_whatsapp_message(
                                    CANDIDATE_PHONE,
                                    f"Hi 👋 Available slots:\n{message}\n\nReply with ONE slot (e.g. 4pm)"
                                )

                            # =========================
                            # ✅ CANDIDATE FLOW
                            # =========================
                            elif sender.endswith(CANDIDATE_PHONE[-10:]):
                                print("📌 Candidate detected")

                                db = SessionLocal()

                                interview = db.query(Interview)\
                                    .order_by(Interview.id.desc())\
                                    .first()

                                if interview:
                                    interview.selected_slot = message
                                    interview.status = "confirmed"
                                    db.commit()

                                    print("🚀 Creating calendar event...")

                                    try:
                                        # convert "4pm" → datetime
                                        selected_time = datetime.strptime(message, "%I%p")

                                        create_event(
                                            "malvikaa.1708@gmail.com",
                                            "tamannasharma336@gmail.com",
                                            selected_time
                                        )

                                        # ✅ Send confirmation AFTER selection
                                        send_whatsapp_message(
                                            MANAGER_PHONE,
                                            f"✅ Candidate selected: {message}"
                                        )

                                        send_whatsapp_message(
                                            CANDIDATE_PHONE,
                                            f"🎉 Interview confirmed for {message}"
                                        )

                                    except Exception as e:
                                        print("❌ Time parsing error:", e)

                                else:
                                    print("⚠️ No interview found")

                                db.close()

                            else:
                                print("⚠️ Unknown sender")

        except Exception as e:
            print("❌ ERROR:", str(e))

        return "EVENT_RECEIVED", 200


# 🚀 Run local
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
