import os
import requests
from flask import Flask, request

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


# 🔹 Send Slots Message to Manager
def send_startup_message():
    print("🚀 FUNCTION CALLED")

    if not ACCESS_TOKEN:
        print("❌ ACCESS TOKEN MISSING")

    if not PHONE_NUMBER_ID:
        print("❌ PHONE NUMBER ID MISSING")

    message = "Hi 👋 What are your free interview slots today?"

    print("📨 Sending message now...")
    send_whatsapp_message(MANAGER_PHONE, message)



# 🔹 Run once safely
def send_once_on_start():
    if not hasattr(app, "already_sent"):
        send_startup_message()
        app.already_sent = True


# 🔥 SAFE TRIGGER (NO CRASH)
@app.before_request
def run_once():
    if not hasattr(app, "startup_done"):
        print("🚀 First request → sending startup message")
        send_once_on_start()
        app.startup_done = True


# ✅ Home Route
@app.route("/")
def home():
    return "Server running ✅"


# ✅ Test Route
@app.route("/test")
def test():
    return "Test route working ✅"


# ✅ Manual trigger
@@app.route("/send-slots")
def send_slots():
    print("🔥 HARD TEST ROUTE HIT")

    send_whatsapp_message(
        MANAGER_PHONE,
        "🔥 TEST MESSAGE FROM RAILWAY"
    )

    return "Test message sent"

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
                            sender = msg.get("from")

                            if msg.get("type") == "text":
                                message = msg.get("text", {}).get("body")
                            else:
                                message = "Unsupported message"

                            print("💬 Message:", message)
                            print("👤 Sender:", sender)

                            # ✅ Manager sends slots
                            if sender == MANAGER_PHONE:
                                slots = message

                                send_whatsapp_message(
                                    CANDIDATE_PHONE,
                                    f"Hi 👋 Available interview slots are:\n{slots}\n\nReply with your preferred time."
                                )

                            # ✅ Candidate selects slot
                            elif sender == CANDIDATE_PHONE:
                                selected_slot = message

                                send_whatsapp_message(
                                    MANAGER_PHONE,
                                    f"✅ Candidate selected: {selected_slot}"
                                )

                                send_whatsapp_message(
                                    CANDIDATE_PHONE,
                                    f"🎉 Interview confirmed for {selected_slot}"
                                )

        except Exception as e:
            print("❌ ERROR:", str(e))

        return "EVENT_RECEIVED", 200


# 🚀 Local run only
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
