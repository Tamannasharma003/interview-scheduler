import os
import requests
from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = "tamanna_verify_token"

ACCESS_TOKEN = "EAALHZAkuHdf8BQ0KZB8tR5Kxy70bqAR0pTaYnKVFiKvWQe8AsDGphStHoRKhZAGNzwFZAfHhFZChE4kaAc3K0t4TahWZA9YI8aXTXV4PnCFTENjNZAoKzsU4BCunEI82c8CAsZBWAUAS1zyLH9BLwtogC7IoYKvnt12K1fIjPK4esMSDBLg1XUUQbYBiHraZBLS56wBSpezGxoQUPfZCmAi3v1OgwQAZBk1D9VrlgkRf2WM4fcXPOUDWMTomczvqE4ZAXYjBgOVPeR3e5o5oYSLAtmN4HOZBE"
PHONE_NUMBER_ID = "1133619556482851"


def send_whatsapp_message(to, message):
    print("Sending message to:", to)
    print("Message:", message)

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

    print("STATUS CODE:", response.status_code)
    print("RESPONSE TEXT:", response.text)


@app.route("/")
def home():
    return "Server running"


@app.route("/webhook", methods=["GET", "POST"])
def webhook():

    # ✅ Verification (Meta setup)
  
    # ✅ GET → Verification
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode == "subscribe" and token == VERIFY_TOKEN:
            return str(challenge), 200
        else:
            return "Verification failed", 403

    # ✅ POST → Incoming messages
    if request.method == "POST":
        data = request.json
        print("Incoming message FULL:", data)

        try:
            if "entry" in data:
                for entry in data["entry"]:
                    for change in entry.get("changes", []):
                        value = change.get("value", {})
                        messages = value.get("messages", [])

                        print("DEBUG VALUE:", value)
                        print("DEBUG MESSAGES:", messages)

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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
