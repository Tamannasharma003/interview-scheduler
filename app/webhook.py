import os
import requests
from flask import Flask, request

from database import engine, SessionLocal
from model import Interview
from calendar_service import create_event
from datetime import datetime, timedelta


# ================================
# 🔹 Convert "2pm" → datetime
# ================================
def convert_to_datetime(slot_str):
    now = datetime.now()

    time_obj = datetime.strptime(slot_str.strip().lower(), "%I%p").time()

    start_time = datetime(
        year=now.year,
        month=now.month,
        day=now.day,
        hour=time_obj.hour,
        minute=time_obj.minute
    )

    if start_time < now:
        start_time = start_time + timedelta(days=1)

    return start_time


# ================================
# 🔹 Setup
# ================================
Interview.metadata.create_all(bind=engine)

app = Flask(__name__)

VERIFY_TOKEN = "tamanna_verify_token"

ACCESS_TOKEN = os.getenv("whatsapp_token")
PHONE_NUMBER_ID = os.getenv("phone_number_id")

MANAGER_PHONE = "918168100074"
CANDIDATE_PHONE = "919910105877"


# ================================
# 🔹 Send WhatsApp Message
# ================================
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


# ================================
# 🔹 Startup Message
# ================================
def send_startup_message():
    print("🚀 Sending startup message")

    send_whatsapp_message(
        MANAGER_PHONE,
        "Hi 👋 What are your free interview slots today?"
    )


@app.before_request
def run_once():
    if not hasattr(app, "startup_done"):
        send_startup_message()
        app.startup_done = True


# ================================
# 🔹 Routes
# ================================
@app.route("/")
def home():
    return "Server running ✅"


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
                                    available_slots = interview.slots.lower().replace(",", " ").split()
                                    selected_slot = message.lower().strip()

                                    # Normalize spaces (2 pm → 2pm)
                                    selected_slot = selected_slot.replace(" ", "")
                                    available_slots = [s.replace(" ", "") for s in available_slots]

                                    print("📌 Available:", available_slots)
                                    print("📌 Selected:", selected_slot)

                                    # ❌ INVALID SLOT
                                    if selected_slot not in available_slots:
                                        print("❌ Invalid slot selected")

                                        send_whatsapp_message(
                                            CANDIDATE_PHONE,
                                            f"❌ Invalid slot.\nPlease choose from:\n{interview.slots}"
                                        )

                                        db.close()
                                        return "ok", 200

                                    # ✅ VALID SLOT
                                    interview.selected_slot = selected_slot
                                    interview.status = "confirmed"
                                    db.commit()

                                    print("🚀 Creating calendar event...")

                                    try:
                                        start_time = convert_to_datetime(selected_slot)

                                        create_event(
                                            "malvikaa.1708@gmail.com",
                                            "tamannasharma336@gmail.com",
                                            start_time
                                        )

                                        # Notify Manager
                                        send_whatsapp_message(
                                            MANAGER_PHONE,
                                            f"✅ Candidate selected: {selected_slot}"
                                        )

                                        # Notify Candidate
                                        send_whatsapp_message(
                                            CANDIDATE_PHONE,
                                            f"🎉 Interview confirmed for {selected_slot}"
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


# ================================
# 🚀 Run
# ================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
