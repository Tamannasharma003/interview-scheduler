import os
import requests
from flask import Flask, request

app = Flask(__name__)

with app.app_context():
    print("🚀 App started (Railway detected)")
    send_once_on_start()


VERIFY_TOKEN = "tamanna_verify_token"

ACCESS_TOKEN = os.getenv("whatsapp_token")
PHONE_NUMBER_ID = os.getenv("phone_number_id")

# ✅ Manager number (NO +)
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
    print("STATUS:", response.status_code)
    print("RESPONSE:", response.text)


# 🔹 Startup Message Function (THIS WAS MISSING)
def send_startup_message():
    print("🚀 Sending message to manager...")
    message = "Hi 👋 What are your free interview slots today?"
    send_whatsapp_message(MANAGER_PHONE, message)


# 🔹 Run only once on deploy
def send_once_on_start():
    if not os.path.exists("sent_flag.txt"):
        send_startup_message()
        with open("sent_flag.txt", "w") as f:
            f.write("sent")


# ✅ Home Route (manual trigger)
@app.route("/")
def home():
    print("🏠 Home route hit")
    send_startup_message()
    return "Server running ✅"


# ✅ Webhook
@app.route("/webhook", methods=["GET", "POST"])
def webhook():

    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode == "subscribe" and token == VERIFY_TOKEN:
            return str(challenge), 200
        else:
            return "Verification failed", 403

    if request.method == "POST":
        data = request.json
        print("Incoming:", data)

        try:
            if "entry" in data:
                for entry in data["entry"]:
                    for change in entry.get("changes", []):
                        value = change.get("value", {})
                        messages = value.get("messages", [])

                        if messages:
                            msg = messages[0]
                            message = msg.get("text", {}).get("body")
                            sender = msg.get("from")

                            print("Message:", message)
                            print("Sender:", sender)

                            reply = f"Hello Tamanna 👋 You said: {message}"
                            send_whatsapp_message(sender, reply)

        except Exception as e:
            print("ERROR:", str(e))

        return "EVENT_RECEIVED", 200


# 🚀 Run app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    print("🚀 Server starting...")

    send_once_on_start()

    app.run(host="0.0.0.0", port=port)
