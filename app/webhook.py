import requests

ACCESS_TOKEN = "EAALHZAkuHdf8BQ0qQe1Pj0yEdwjgIchpZAgDkdkUyAfKGa0s3cSf6PcEGAGEXgUaPHyJhoSOzUlaJXB0L7HxgMFuCQQmsa3irXTyuYq3rrV5U6iZA9gmZA1cSJqi9rJqYFVwTFuElBAFdpfVZBbl90fpZBr0WVnOEHHsiLWMM1ZAZCo5DJBZCDprJYPD4rKgljW6szsmPob9vQ6QYiL2Benp8SKZBgehaewAuZB6ZCjoxWqsiM9dmkICQXFSH1mHNBB9PAs6qXUzB8lYqRpsWTC9b5rgiuyWZBAZDZD"
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

