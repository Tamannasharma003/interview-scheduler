from flask import Flask

app = Flask(__name__)

# Import webhook routes AFTER creating app
import webhook


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Railway PORT
    print("🚀 Starting main app...")
    app.run(host="0.0.0.0", port=port)
    @app.route("/")
    def home():
     return "Server running ✅"


