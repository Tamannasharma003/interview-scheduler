import os
import requests
from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = "tamanna_verify_token"

ACCESS_TOKEN = "EAALHZAkuHdf8BQ108wH6WKnPrA6LjAWPPHZBXrUrSDmLOpbnSNRF6FMwMrCHmSX6pKjbb7nubLUj843mgxgfUIhgLYOSmu4Xen9w6Apw9tIBEo57GIZCGanX1E79PZBQeZAUCu45VYArSIBk1x1gACDOhPowM5v4ZBx7l5i6kFhEHhb9nUZARgOyZASc68DPuXicd4YUBJw7SEPOyPmKxIyUtEWd0PZBSFQa8DP3ZAItNDifYXaC4z5B7AR3hGqsGVLfHP4EKPFjYZBKBXjfBVOwmsDNMJE"
PHONE_NUMBER_ID = "1133619556482851"


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
        "text": {
            "body": message
        }
    }

    response = requests.post(url, headers=headers, json=data)
    print(response.json())


@app.route("/")
def home():
    return "Server running"


@app.route("/webhook", methods=["GET", "POST"])
def webhook():

    # WhatsApp verification
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode == "subscribe" and token == VERIFY_TOKEN:
            return str(challenge), 200
        else:
            return "Verification failed", 403

    # When WhatsApp sends a message
    if request.method == "POST":

        data = request.json
        print("Incoming message:", data)

        try:
            message = data["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]
            sender = data["entry"][0]["changes"][0]["value"]["messages"][0]["from"]

            print("Message:", message)
            print("Sender:", sender)

            reply = f"Hello 👋 Tamanna! You said: {message}"

            send_whatsapp_message(sender, reply)

        except Exception as e:
            print("Error:", e)

        return "EVENT_RECEIVED", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
