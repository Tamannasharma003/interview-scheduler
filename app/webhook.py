import os
import requests
from flask import Flask, request

from database import engine, SessionLocal
from model import Interview
from calendar_service import create_event 

from datetime import datetime
import json


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

    print("📤 Sent:", response.status_code, response.text)


# ================================
# 🔹 Routes
# ================================
@app.route("/webhook", methods=["GET", "POST"])
def webhook():

    # 🔹 Verification
    if request.method == "GET":
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return "Error", 403

    # 🔹 Incoming Messages
    if request.method == "POST":
        data = request.json
        print("📥 Incoming:", data)

        try:
            for entry in data.get("entry", []):
                for change in entry.get("changes", []):
                    value = change.get("value", {})

                    if "messages" not in value:
                        continue

                    msg = value["messages"][0]

                    sender = msg.get("from", "").strip()

                    if msg.get("type") == "text":
                        message = msg["text"]["body"].strip()
                    else:
                        message = ""

                    print("👤 Sender:", sender)
                    print("💬 Message:", message)

                    db = SessionLocal()

                    # =========================
                    # ✅ MANAGER FLOW
                    # =========================
                    if sender.endswith(MANAGER_PHONE[-10:]):

                        print("📌 Manager detected")

                        # Convert message → list
                        slots = [s.strip() for s in message.split(",")]

                        new_interview = Interview(
                            manager_id=MANAGER_PHONE,
                            candidate_id=CANDIDATE_PHONE,
                            job_id=1,   # ✅ Linked to jobs table
                            manager_slots=json.dumps(slots),
                            status="slots_received"
                        )

                        db.add(new_interview)
                        db.commit()
                        db.close()   # ✅ FIXED

                        send_whatsapp_message(
                            CANDIDATE_PHONE,
                            f"""Hi 👋 Available slots:

{chr(10).join(slots)}

Reply with one slot (example: 2026-04-01 15:00)"""
                        )

                    # =========================
                    # ✅ CANDIDATE FLOW
                    # =========================
                    elif sender.endswith(CANDIDATE_PHONE[-10:]):

                        print("📌 Candidate detected")

                        interview = db.query(Interview)\
                            .order_by(Interview.id.desc())\
                            .first()

                        if not interview:
                            db.close()
                            return "ok", 200

                        # ✅ Prevent crash
                        if not interview.manager_slots:
                            db.close()
                            return "ok", 200

                        slots = json.loads(interview.manager_slots)

                        selected = message.strip()

                        print("📌 Available:", slots)
                        print("📌 Selected:", selected)

                        # ❌ Invalid slot
                        if selected not in slots:
                            send_whatsapp_message(
                                CANDIDATE_PHONE,
                                f"❌ Invalid slot.\nChoose from:\n{chr(10).join(slots)}"
                            )
                            db.close()
                            return "ok", 200

                        # ✅ Valid slot
                        selected_dt = datetime.strptime(selected, "%Y-%m-%d %H:%M")

                        interview.selected_slot = selected_dt
                        interview.status = "scheduled"

                        db.commit()
                        db.close()   # ✅ FIXED

                        print("🚀 Creating calendar event...")

                        # 🚀 Create Calendar Event
                        create_event(
                            "malvikaa.1708@gmail.com",
                            "tamannasharma336@gmail.com",
                            selected_dt
                        )

                        # Notify Manager
                        send_whatsapp_message(
                            MANAGER_PHONE,
                            f"✅ Candidate selected: {selected}"
                        )

                        # Notify Candidate
                        send_whatsapp_message(
                            CANDIDATE_PHONE,
                            f"🎉 Interview confirmed for {selected}"
                        )

                    else:
                        db.close()
                        print("⚠️ Unknown sender")

        except Exception as e:
            print("❌ ERROR:", e)

        return "EVENT_RECEIVED", 200


# ================================
# 🚀 Run
# ================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
