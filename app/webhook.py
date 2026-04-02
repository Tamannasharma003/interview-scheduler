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

    # 🔥 FIX: add space before am/pm if missing
    slot_str = slot_str.replace("am", " am").replace("pm", " pm")

    # remove double spaces (important)
    slot_str = " ".join(slot_str.split())

    # ✅ Try human formats
    for fmt in ["%d %B %I %p", "%d %b %I %p"]:
        try:
            dt = datetime.strptime(slot_str, fmt)
            return dt.replace(year=now.year)
        except:
            continue

    # fallback
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
# 🔹 Startup Message (Manager)
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

    message = (
        "👋 Hello!\n\n"
        "You have a new interview request.\n\n"
        f"👤 Candidate: {candidate.name.title()}\n"
        f"📞 Contact: {format_phone(candidate.phone)}\n"
        f"💼 Role: {job.role}\n\n"
        "📅 Please share your available time slots.\n\n"
        "Example:\n"
        "1 April 11 am, 2 April 3 pm"
    )

    send_whatsapp_message(format_phone(manager.phone), message)

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

    # =========================
    # 🔹 Verification
    # =========================
    if request.method == "GET":
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge"), 200
        return "Verification failed", 403

    # =========================
    # 🔹 Incoming Messages
    # =========================
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

            interview = db.query(Interview).order_by(Interview.id.desc()).first()

            candidate = db.query(Candidate).filter(
                Candidate.candidate_id == interview.candidate_id
            ).first()

            manager = db.query(Manager).filter(
                Manager.manager_id == interview.manager_id
            ).first()

            job = db.query(Job).filter(
                Job.id == interview.job_id
            ).first()

            # =========================
            # ✅ MANAGER FLOW
            # =========================
            if sender == manager.phone[-10:]:
                print("📌 Manager detected")

                slots = [s.strip() for s in message.split(",")]

                interview.manager_slots = json.dumps(slots)
                interview.status = "slots_received"
                db.commit()

                send_whatsapp_message(
                    format_phone(candidate.phone),
                    f"👋 Hello {candidate.name.title()},\n\n"
                    f"Your interview for *{job.role}* has been scheduled.\n\n"
                    "📅 Available Slots:\n" +
                    "\n".join(slots) +
                    "\n\nPlease reply with your preferred time."
                )

            # =========================
            # ✅ CANDIDATE FLOW
            # =========================
            elif sender == candidate.phone[-10:]:
                print("📌 Candidate detected")

                slots = json.loads(interview.manager_slots)
                selected_slot = message.strip()

                normalized_slots = [s.lower().replace(" ", "") for s in slots]
                selected_clean = selected_slot.lower().replace(" ", "")

                if selected_clean not in normalized_slots:
                    send_whatsapp_message(
                        format_phone(candidate.phone),
                        "❌ Invalid slot.\n\nAvailable options:\n" + "\n".join(slots)
                    )
                    return "ok", 200

                start_time = convert_to_datetime(selected_slot)

                interview.selected_slot = start_time
                interview.status = "scheduled"
                db.commit()

                print("🚀 Creating calendar event...")

                try:
                    create_event(
                        manager.email,
                        candidate.email,
                        start_time
                    )
                except Exception as e:
                    print("❌ Calendar error:", e)

                # =========================
                # 🎯 PROFESSIONAL MESSAGE
                # =========================

                manager_msg = (
                    "📌 Interview Confirmed\n\n"
                    f"👤 Candidate: {candidate.name.title()}\n"
                    f"📞 Phone: {format_phone(candidate.phone)}\n"
                    f"💼 Role: {job.role}\n\n"
                    f"📅 Date: {selected_slot}\n\n"
                    "📧 Calendar invite sent."
                )

                candidate_msg = (
                    "🎉 Interview Scheduled\n\n"
                    f"👤 Candidate: {candidate.name.title()}\n"
                    f"💼 Role: {job.role}\n\n"
                    f"📅 Date: {selected_slot}\n\n"
                    "📧 You will receive a calendar invite shortly.\n\n"
                    "Best of luck 👍"
                )

                send_whatsapp_message(format_phone(manager.phone), manager_msg)
                send_whatsapp_message(format_phone(candidate.phone), candidate_msg)

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
