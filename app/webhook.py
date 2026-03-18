import os
import requests
from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = "tamanna_verify_token"

ACCESS_TOKEN = os.getenv("whatsapp_token")
PHONE_NUMBER_ID = os.getenv("phone_number_id")

# ✅ Manager number (no + sign)
MANAGER_PHONE = "918168100074"


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


# 🔹 Send Slots Message
def send_startup_message():
    print("🚀 Sending slots message...")
    message = "Hi 👋 What are your free interview slots today?"
    send_whatsapp_message(MANAGER_PHONE, message)


# ✅ Home Route
@app.route("/")
def home():
    print("🏠 Home route hit")
    return "Server running ✅"


# ✅ TEST ROUTE (VERY IMPORTANT FOR DEBUG)
@app.route("/test")
def test():
    print("🔥 TEST ROUTE WORKING")
    return "Test route working ✅"


# ✅ SEND SLOTS ROUTE
@app.route("/send-slots")
def send_slots():
    print("🔥🔥🔥 /send-slots HIT")
    send_startup_message()
    return "Slots sent successfully ✅"


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

                            reply = f"Hello Tamanna 👋 You said: {message}"
                            send_whatsapp_message(sender, reply)

                        else:
                            print("📌 Status update ignored")

        except Exception as e:
            print("❌ ERROR:", str(e))

        return "EVENT_RECEIVED", 200


# 🚀 Run app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print("🚀 Server starting...")
    app.run(host="0.0.0.0", port=port)
