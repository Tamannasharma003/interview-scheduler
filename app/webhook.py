import requests

ACCESS_TOKEN = "EAALHZAkuHdf8BQwLx34Vkmebvl5Ht0PouKktlG7rw8vZBRwYKZAMHi5iW35sNM2cRaHzygBDEzhtFgSiNUaTzCdI1NaiHDUgMO0dOnIAzAO5wcmfgKtcYrotaVr0OLHAecESj2AEM66dG7zrNZC9wgwGlH5WfpWZBeXyDgDkTzELB4Xc2XCxrzmK7tqwmJUqeVdZCxNEwHlcKQbWKLLOj41Nzml2mQJtRQweiFcgX6K8lfRhEpCZA5g3HlYUPPrK08x7XI0J0ETv4oxGI5Q7g1EzqFi5QZDZD"
PHONE_NUMBER_ID = "1133619556482851"

@app.route("/webhook", methods=["GET","POST"])
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
            phone = data["entry"][0]["changes"][0]["value"]["messages"][0]["from"]
            text = data["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]

            send_message(phone, "Hello! Your message received.")
        except:
            pass

        return "EVENT_RECEIVED", 200
    def send_message(phone, message):

    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "text",
        "text": {"body": message}
    }

    requests.post(url, headers=headers, json=payload)

