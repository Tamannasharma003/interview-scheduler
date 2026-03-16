from flask import Flask, request, jsonify

app = Flask(__name__)

VERIFY_TOKEN = "tamanna_verify_token"


@app.route("/webhook", methods=["GET"])
def verify():
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if token == VERIFY_TOKEN:
        return challenge
    return "Verification failed"


@app.route("/webhook", methods=["POST"])
def receive_message():
    data = request.json
    print("Message received:")
    print(data)

    return jsonify({"status": "received"}), 200


if __name__ == "__main__":
    app.run(port=5000)
