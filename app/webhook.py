import os
import requests
from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = "tamanna_verify_token"

ACCESS_TOKEN = "EAALHZAkuHdf8BQwLx34Vkmebvl5Ht0PouKktlG7rw8vZBRwYKZAMHi5iW35sNM2cRaHzygBDEzhtFgSiNUaTzCdI1NaiHDUgMO0dOnIAzAO5wcmfgKtcYrotaVr0OLHAecESj2AEM66dG7zrNZC9wgwGlH5WfpWZBeXyDgDkTzELB4Xc2XCxrzmK7tqwmJUqeVdZCxNEwHlcKQbWKLLOj41Nzml2mQJtRQweiFcgX6K8lfRhEpCZA5g3HlYUPPrK08x7XI0J0ETv4oxGI5Q7g1EzqFi5QZDZD"
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
        "text": {"body": message}
    }

    requests.post(url, headers=headers, json=data)


@app.route("/")
def home():
    return "Server running"


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
        print(data)

        try:
            message = data["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]
            sender = data["entry"][0]["changes"][0]["value"]["messages"][0]["from"]

            reply = f"You said: {message}"

            send_whatsapp_message(sender, reply)

        except:
            pass

        return "EVENT_RECEIVED", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

