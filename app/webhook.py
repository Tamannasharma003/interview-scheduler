import os
import requests
from flask import request

from database import engine, get_db
from model import Interview, Candidate, Manager, Job
from calendar_service import create_event

from datetime import datetime
import json
from app import app


# ================================
# 🔹 Format phone
# ================================
def format_phone(phone):
    phone = phone.replace("+", "").strip()
    return "91" + phone[-10:]


# ================================
# 🔹 Convert slot → datetime
# ================================
def convert_to_datetime(slot_str):
    now = datetime.now()
    slot_str = slot_str.lower().strip()

    for fmt in ["%d %B %I %p", "%d %b %I %p"]:
        try:
            dt = datetime.strptime(slot_str, fmt)
            return dt.replace(year=now.year)
        except:
            continue

    try:
        return datetime.strptime(slot_str, "%Y-%m-%d %H:%M")
    except:
        pass

    raise ValueError("Invalid date format")


# ================================
# 🔹 Setup
# ================================
Interview.metadata.create_all(bind=engine)

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

    print("📤 Sent to:", to)
    print("💬 Message:", message)
    print("STATUS:", response.status_code)
    print("RESPONSE:", response.text)


# ================================
# 🔹 Startup Message
# ================================
def send_startup_message():
    print("🚀 Sending startup message")

    db = next(get_db())

    interview = db.query(Interview).order_by(Interview.id.desc()).first()

    if not interview:
        print("❌ No interview found")
        db.close()
        return

    candidate = db.query(Candidate).filter(
        Candidate.candidate_id == interview.candidate_id
    ).first()

    manager = db.query(Manager).filter(
        Manager.manager_id == interview.manager_id
    ).first()

    job = db.query(Job).filter(
        Job.id == interview.job_id
    ).first()

    if not candidate or not manager or not job:
        print("❌ Missing data")
        db.close()
        return

    send_whatsapp_message(
        format_phone(manager.phone),
        f"Hi 👋 What are your available interview slots for {candidate.name} ({job.role})?\n\n"
        "Send like:\n1 April 11 am, 2 April 3 pm"
    )

    db.close()


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

    if request.method == "GET":
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge"), 200
        return "Verification failed", 403

    if request.method == "POST":
        data = request.json
        print("📥 Incoming:", data)

        try:
            entry = data["entry"][0]
            change = entry["changes"][0]
            value = change["value"]

            if "messages" not in value:
                return "ok", 200

            msg = value["messages"][0]
            sender = msg["from"][-10:]
            message = msg["text"]["body"].strip()

            print("👤 Sender:", sender)
            print("💬 Message:", message)

            db = next(get_db())

            # =========================
            # ✅ MANAGER FLOW
            # =========================
            if sender == MANAGER_PHONE[-10:]:
                print("📌 Manager detected")

                interview = db.query(Interview).order_by(Interview.id.desc()).first()

                slots = [s.strip() for s in message.split(",")]

                interview.manager_slots = json.dumps(slots)
                interview.status = "slots_received"
                db.commit()

                candidate = db.query(Candidate).filter(
                    Candidate.candidate_id == interview.candidate_id
                ).first()

                job = db.query(Job).filter(
                    Job.id == interview.job_id
                ).first()

                send_whatsapp_message(
                    format_phone(candidate.phone),
                    f"Hi 👋 Interview for {candidate.name} ({job.role})\n\n"
                    "Available slots:\n" +
                    "\n".join(slots) +
                    "\n\nReply with ONE slot exactly."
                )

            # =========================
            # ✅ CANDIDATE FLOW
            # =========================
            elif sender == CANDIDATE_PHONE[-10:]:
                print("📌 Candidate detected")

                interview = db.query(Interview).order_by(Interview.id.desc()).first()

                if not interview or not interview.manager_slots:
                    print("❌ No slots found")
                    return "ok", 200

                slots = json.loads(interview.manager_slots)
                selected_slot = message.strip()

                # 🔥 SMART MATCHING
                normalized_slots = [s.lower().replace(" ", "") for s in slots]
                selected_clean = selected_slot.lower().replace(" ", "")

                if selected_clean not in normalized_slots:
                    send_whatsapp_message(
                        format_phone(CANDIDATE_PHONE),
                        f"❌ Invalid slot.\nChoose from:\n" + "\n".join(slots)
                    )
                    return "ok", 200

                start_time = convert_to_datetime(selected_slot)

                interview.selected_slot = start_time
                interview.status = "scheduled"
                db.commit()

                manager = db.query(Manager).filter(
                    Manager.manager_id == interview.manager_id
                ).first()

                candidate = db.query(Candidate).filter(
                    Candidate.candidate_id == interview.candidate_id
                ).first()

                print("🚀 Creating calendar event...")

                try:
                    create_event(
                        manager.email,
                        candidate.email,
                        start_time
                    )
                except Exception as e:
                    print("❌ Calendar error:", e)

                # ✅ ALWAYS SEND CONFIRMATION
                send_whatsapp_message(
                    format_phone(manager.phone),
                    f"✅ Candidate selected: {selected_slot}"
                )

                send_whatsapp_message(
                    format_phone(candidate.phone),
                    f"🎉 Interview confirmed for {selected_slot}"
                )

            db.close()

        except Exception as e:
            print("❌ ERROR:", str(e))

        return "EVENT_RECEIVED", 200


# ================================
# 🚀 Run
# ================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
